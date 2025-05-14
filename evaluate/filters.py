def illegal_filter(collected_data):
    filtered_data = {}
    removed_data = {}

    for model, control_methods in collected_data.items():
        filtered_data[model] = {}
        removed_data[model] = {}

        for control_method, length_constraints in control_methods.items():
            filtered_data[model][control_method] = {}
            removed_data[model][control_method] = {}

            for length_constraint, data_entries in length_constraints.items():
                filtered_entries = []
                removed_entries = []

                for entry in data_entries:
                    word_count = entry.get("word_count")
                    if word_count is None:
                        continue
                    if word_count <= 1:
                        removed_entries.append(entry)
                    else:
                        filtered_entries.append(entry)

                if filtered_entries:
                    filtered_data[model][control_method][length_constraint] = filtered_entries

                if removed_entries:
                    removed_data[model][control_method][length_constraint] = removed_entries

    return filtered_data, removed_data
