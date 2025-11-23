
def choose_mapping(node: Dict[str, Any]) -> Dict[str, Any]:
    """Return mapping dict for a single node according to the conditions."""
    external_id: Optional[str] = node.get("externalId")
    name: Optional[str] = node.get("name")
    native_type: str = node.get("nativeType", "unknown")
    region: Optional[str] = node.get("region")

    graph_entity: Dict[str, Any] = node.get("graphEntity", {}) or {}
    ge_name: Optional[str] = graph_entity.get("name")
    ge_props: Dict[str, Any] = graph_entity.get("properties", {}) or {}

    prop_external_id: Optional[str] = ge_props.get("externalId")
    prop_provider_uid: Optional[str] = ge_props.get("providerUniqueId")

    mapping: Dict[str, Any] = {
        "service": native_type,
        "id": "",
        "name": "",
        "arn": "",
        "global_resource": False,
    }

    # CONDITION 1
    if (
        (matches(external_id, prop_provider_uid) or matches(external_id, prop_external_id))
        and has_arn_prefix(external_id)
    ):
        mapping["arn"] = PLACEHOLDER
        return mapping

    # CONDITION 2
    if (
        not has_arn_prefix(external_id)
        and matches(name, ge_name)
        and has_arn_prefix(prop_provider_uid)
    ):
        mapping["arn"] = PLACEHOLDER
        return mapping

    # CONDITION 3 & 4 share initial logic (region decides global flag)
    if not has_arn_prefix(external_id) and (
        matches(name, ge_name)
        or matches(name, prop_external_id)
        or matches(name, prop_provider_uid)
    ):
        mapping["id"] = PLACEHOLDER
        if region in ("", None):
            mapping["global_resource"] = True  # Condition 4
        return mapping

    # CONDITION 5
    if external_id and external_id.count("##") >= 2:
        mapping["arn"] = PLACEHOLDER
        return mapping

    # CONDITION 6
    if (
        not has_arn_prefix(external_id)
        and (
            matches(name, ge_name)
            or matches(name, prop_external_id)
            or prop_provider_uid is None
        )
        and not has_arn_prefix(ge_name)
        and not has_arn_prefix(prop_external_id)
        and (prop_provider_uid is None or not has_arn_prefix(prop_provider_uid))
    ):
        api_info = external_api_stub(node)  # external API call placeholder
        if api_info.get("resourceId") == api_info.get("resourceName"):
            mapping["id"] = PLACEHOLDER
        else:
            mapping["name"] = PLACEHOLDER
        return mapping

    # DEFAULT
    mapping["arn"] = PLACEHOLDER
    return mapping


def generate_mappings(data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Produce final mapping keyed by nativeType."""
    result: Dict[str, Dict[str, Any]] = {}

    nodes = (
        data.get("data", {})
        .get("cloudResourcesv2", {})
        .get("nodes", [])
    )

    for node in nodes:
        native_type = node.get("nativeType", "unknown")
        mapping = choose_mapping(node)

        # If multiple nodes share the same nativeType keep first seen.
        # You can change this behaviour as needed (e.g. list).
        result.setdefault(native_type, mapping)

    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate wiz_resource_to_identifier.json from one or more GraphQL response files"
    )
    parser.add_argument("inputs", nargs="+", type=Path, help="Response JSON file(s) per Wiz native type")
    parser.add_argument("-o", "--output", type=Path, default=Path("wiz_resource_to_identifier.json"))
    args = parser.parse_args()

    combined_mappings: Dict[str, Any] = {}
    for input_path in args.inputs:
        try:
            with input_path.open("r", encoding="utf-8") as f:
                response_json = json.load(f)
        except FileNotFoundError:
            print(f"Input file not found: {input_path}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as exc:
            print(f"Invalid JSON in {input_path}: {exc}", file=sys.stderr)
            sys.exit(1)

        combined_mappings.update(generate_mappings(response_json))

    # Write consolidated output once all inputs processed
    with args.output.open("w", encoding="utf-8") as f:
        f.write("// System generated. DON'T EDIT this file\n")
        json.dump(combined_mappings, f, indent=2)

    print(f"Generated {args.output} with {len(combined_mappings)} mapping(s)")


if __name__ == "__main__":
    main()
