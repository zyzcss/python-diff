import re


class Diff:
    def __init__(self, old_string, new_string):
        self.old_string = self.remove_empty(self.tokenize(old_string))
        self.new_string = self.remove_empty(self.tokenize(new_string))

    def tokenize(self, value):
        ret_lines = []
        lines_and_newlines = re.split("(\n|\r\n)", value)
        if not lines_and_newlines[-1]:
            lines_and_newlines.pop()

        for i, line in enumerate(lines_and_newlines):
            if i % 2:
                ret_lines[-1] += line
            else:
                ret_lines.append(line)
        return ret_lines

    def equals(self, left, right):
        return left == right

    def push_component(self, components, added, removed):
        last = components[-1] if len(components) > 0 else False
        if last and last.get('added') == added and last.get('removed') == removed:
            components[-1] = {'count': last.get('count') + 1, 'added': added, 'removed': removed}
        else:
            components.append({'count': 1, 'added': added, 'removed': removed})

    def extract_common(self, base_path, new_string, old_string, diagonal_path):
        new_len = len(new_string)
        old_len = len(old_string)
        new_pos = base_path.get('new_pos')
        old_pos = new_pos - diagonal_path

        common_count = 0

        while new_pos + 1 < new_len and old_pos + 1 < old_len and self.equals(new_string[new_pos + 1],
                                                                              old_string[old_pos + 1]):
            new_pos += 1
            old_pos += 1
            common_count += 1

        if common_count:
            base_path.get('components').append({'count': common_count})

        base_path['new_pos'] = new_pos
        return old_pos

    def remove_empty(self, array):
        ret = []
        for arr in array:
            if arr:
                ret.append(arr)
        return ret

    def join(self, chars):
        return ''.join(chars)

    def run(self):
        old_string = self.old_string
        new_string = self.new_string

        old_len = len(old_string)
        new_len = len(new_string)
        # 编辑长度
        self.edit_len = 1
        max_len = old_len + new_len

        best_path = {0: {'new_pos': -1, 'components': []}}

        old_pos = self.extract_common(best_path.get(0), new_string, old_string, 0)
        if best_path.get(0).get('new_pos') + 1 >= new_len and old_pos + 1 >= old_len:
            return [{'value': ''.join(new_string), 'count': len(new_string)}]

        def build_values(diff, components, new_string, old_string, use_longest_token):
            component_pos = 0
            component_len = len(components)
            _new_pos = 0
            _old_pos = 0

            while component_pos < component_len:
                component = components[component_pos]
                count = component.get('count')
                if not component.get('removed'):
                    component['value'] = ''.join(new_string[_new_pos: _new_pos + count])
                    _new_pos += count

                    if not component.get('added'):
                        _old_pos += count
                else:
                    component['value'] = ''.join(old_string[_old_pos: _old_pos + count])
                    _old_pos += count
                    if component_pos and components[component_pos - 1].get('added'):
                        tmp = components[component_pos - 1]
                        components[component_pos - 1] = components[component_pos]
                        components[component_pos] = tmp
                component_pos += 1

            last_component = components[component_len - 1]
            if component_len > 1 and type(last_component.get('value')) == str and (
                    last_component.get('added') or last_component.get('removed')) and '' == last_component.get(
                                                                                                      'value'):
                components[component_len - 2]['value'] += last_component.get('value')
                components.pop()
            return components

        def clone_path(path):
            return {
                'new_pos': path.get('new_pos'),
                'components': path.get('components').copy(),
            }

        def exec_edit_length(self):
            diagonal_path = -1 * self.edit_len
            while diagonal_path <= self.edit_len:
                base_path = False
                add_path = best_path.get(diagonal_path - 1)
                remove_path = best_path.get(diagonal_path + 1)
                _old_pos = (remove_path.get('new_pos') if remove_path else 0) - diagonal_path

                if add_path:
                    best_path[diagonal_path - 1] = False

                can_add = add_path and add_path.get('new_pos') + 1 < new_len
                can_remove = remove_path and (0 <= _old_pos) and (_old_pos < old_len)

                if not can_add and not can_remove:
                    best_path[diagonal_path] = False
                    diagonal_path += 2
                    continue

                if not can_add or (can_remove and add_path.get('new_pos') < remove_path.get('new_pos')):
                    base_path = clone_path(remove_path)
                    self.push_component(base_path.get('components'), False, True)
                else:
                    base_path = add_path
                    base_path['new_pos'] += 1
                    self.push_component(base_path.get('components'), True, False)

                _old_pos = self.extract_common(base_path, new_string, old_string, diagonal_path)

                if (base_path.get('new_pos') + 1) >= new_len and (_old_pos + 1) >= old_len:
                    return build_values(self, base_path.get('components'), new_string, old_string, False)
                else:
                    best_path[diagonal_path] = base_path
                diagonal_path += 2
            self.edit_len += 1

        while self.edit_len <= max_len:
            ret = exec_edit_length(self)
            if ret:
                return ret
        return []
