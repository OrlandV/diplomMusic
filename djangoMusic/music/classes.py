from .ISPager.dict_fetch_all import dict_fetch_all


class Option:
    index = 0

    def __init__(self, value, text: str):
        Option.index += 1
        self.index = Option.index
        self.value = value
        self.text = text


class Form:
    def __init__(self, request, fields, tag_table: bool = True,
                 sub_ok_value: str | None = 'OK', sub_cancel_value: str | None = None):
        self.request = request
        self.html = ''
        # if self.validate_fields(fields):  # Около 100 строк проверки.
        if tag_table:
            self.html += '\n\t\t<table>'
        for name, field in fields.items():
            if field['type'] == 'checkbox':
                self.checkbox(name, field['chbPar'])
                continue
            label_name = '' if 'labelName' not in field or not field['labelName'] else name
            self.html += '\n\t\t\t<tr'
            if 'display' in field and not field['display']:
                self.html += ' style="display: none;"'
            self.html += '>\n\t\t\t\t<td>'
            if 'label' in field and field['label']:
                self.html += field['label']
                if label_name:
                    self.html += ' '
                self.html += label_name
                if field['label'][len(field['label']) - 1] != '?' or label_name:
                    self.html += ':'
            self.html += '</td>\n\t\t\t\t<td>'
            if field['type'] == 'date':
                self.html += f'<input type="date" name="{name}" value="'
                if 'ok' in self.request.GET or 'sub' in self.request.GET:
                    if name in self.request.GET:
                        self.html += self.request.GET.get(name)
                elif 'value' in field:
                    self.html += str(field['value'])
                self.html += '"'
                if 'disabled' in field and field['disabled']:
                    self.html += ' disabled'
                if 'required' in field and field['required']:
                    self.html += ' required'
                self.html += '>'
            elif field['type'] == 'number':
                self.html += f'<input type="number" name="{name}"'
                if 'class' in field and field['class']:
                    self.html += f' class="{field['class']}"'
                if 'disabled' in field and field['disabled']:
                    self.html += ' disabled'
                if 'required' in field and field['required']:
                    self.html += ' required'
                self.html += ' value="'
                if 'ok' in self.request.GET or 'sub' in self.request.GET:
                    if name in self.request.GET:
                        self.html += self.request.GET.get(name)
                    elif 'value' in field:
                        self.html += str(field['value'])
                    elif 'min' in field:
                        self.html += str(field['min'] or 0)
                elif 'value' in field:
                    self.html += str(field['value'])
                elif 'min' in field:
                    self.html += str(field['min'] or 0)
                self.html += '"'
                if 'min' in field and field['min']:
                    self.html += f' min="{field['min']}"'
                if 'max' in field and field['max']:
                    self.html += f' max="{field['max']}"'
                if 'step' in field and field['step']:
                    self.html += f' step="{field['step']}"'
                self.html += '>'
            elif field['type'] == 'selOpt':
                self.html += f'\n\t\t\t\t\t<select name="{name}" id="{name}"'
                if 'class' in field and field['class']:
                    self.html += f' class="{field['class']}"'
                if 'multiple' in field and field['multiple']:
                    self.html += ' multiple'
                if 'disabled' in field and field['disabled']:
                    self.html += ' disabled'
                if 'required' in field and field['required']:
                    self.html += ' required'
                if 'size' in field and field['size']:
                    self.html += f' size="{field['size']}"'
                self.html += '>'
                if 'empty' not in field or field['empty']:
                    self.html += '\n\t\t\t\t\t\t<option value="'
                    if 'emptyValue' in field:
                        self.html += field['emptyValue']
                    self.html += '">'
                    if 'emptyOption' in field:
                        self.html += field['emptyOption']
                    self.html += '</option>'
                if isinstance(field['option'], list):
                    if 'sort' in field and field['sort']:
                        order = field['sort']
                    else:
                        order = field['option'][0]
                else:
                    order = field['option']
                query = f'SELECT {field['fields']} FROM {field['table']} ORDER BY {order}'
                rows = dict_fetch_all(query)
                for dbf in rows:
                    self.html += f'\n\t\t\t\t\t\t<option value="{dbf['id']}"'
                    if (
                        ('ok' in self.request.GET or 'sub' in self.request.GET) and name in self.request.GET and
                        dbf['id'] == int(self.request.GET.get(name))
                    ) or (
                        'selectedValue' in field and field['selectedValue'] and (
                            (
                                isinstance(field['selectedValue'], tuple) and
                                len(field['selectedValue']) == 1 and
                                field['selectedValue'][0] == dbf[field['option']]
                            ) or (
                                isinstance(field['selectedValue'], str) and
                                field['selectedValue'] == dbf[field['option']]
                            )
                        )
                    ):
                        self.html += ' selected'
                    elif 'selectedValue' in field and field['selectedValue'] and (
                        isinstance(field['selectedValue'], tuple) and
                        not isinstance(field['option'], list)
                    ):
                        for fsv in field['selectedValue']:
                            if dbf[field['option']] in fsv:
                                self.html += ' selected'
                                break
                    elif ('ok' in self.request.GET or 'sub' in self.request.GET) and name in self.request.GET:
                        id_list = self.request.GET.getlist(name)
                        if isinstance(id_list, list):
                            for _id in id_list:
                                if dbf['id'] == _id:
                                    self.html += ' selected'
                    elif (
                        'selectedValue' in field and field['selectedValue'] and
                        isinstance(field['selectedValue'], tuple) and isinstance(field['option'], list)
                    ):
                        for op in field['option']:
                            for fsv in field['selectedValue']:
                                if op in fsv:
                                    self.html += ' selected'
                    elif (
                        'selectedId' in field and field['selectedId'] and
                        not isinstance(field['selectedId'], tuple) and field['selectedId'] == dbf['id']
                    ):
                        self.html += ' selected'
                    elif 'selectedId' in field and field['selectedId'] and isinstance(field['selectedId'], tuple):
                        for fsv in field['selectedId']:
                            if dbf['id'] in fsv:
                                self.html += ' selected'
                    self.html += '>'
                    if isinstance(field['option'], list):
                        i = 0
                        st = ''
                        for op in field['option']:
                            if i == 0:
                                s = field['separator'] if 'separator' in field else ' ('
                            else:
                                s = field['separator'] if 'separator' in field else '. '
                            if i == len(field['option']) - 1:
                                s = '' if 'separator' in field else ')'
                            st += str(dbf[op]) + s
                            i += 1
                        ow = field['optionWidth'] if 'optionWidth' in field else 230
                        self.html += st[:ow - 1] + '…' if len(st) > ow else st
                    else:
                        self.html += dbf[field['option']]
                    self.html += '</option>'
                self.html += '\n\t\t\t\t\t</select>'
            elif field['type'] == 'submit':
                self.html += f'<input type="submit" name="{name}" value="{field['value']}">'
            elif field['type'] == 'text':
                self.html += f'<input type="text" name="{name}"'
                if 'class' in field and field['class']:
                    self.html += f' class="{field['class']}"'
                if 'disabled' in field and field['disabled']:
                    self.html += ' disabled'
                if 'required' in field and field['required']:
                    self.html += ' required'
                if 'placeholder' in field and field['placeholder']:
                    self.html += f' placeholder="{field['placeholder']}"'
                if 'size' in field and field['size']:
                    self.html += f' size="{field['size']}"'
                self.html += ' value="'
                if 'ok' in self.request.POST or 'sub' in self.request.GET:
                    if name in self.request.POST:
                        self.html += self.request.POST.get(name).strip()
                    elif name in self.request.GET:
                        self.html += self.request.GET.get(name).strip()
                    elif 'value' in field:
                        self.html += str(field['value'])
                elif 'value' in field:
                    self.html += str(field['value'])
                self.html += '">'
            elif field['type'] == 'time':
                self.html += f'<input type="time" name="{name}" value="'
                if 'ok' in self.request.GET or 'sub' in self.request.GET:
                    if name in self.request.GET:
                        self.html += self.request.GET.get(name)
                elif 'value' in field:
                    self.html += str(field['value'])
                self.html += '"'
                if 'disabled' in field and field['disabled']:
                    self.html += ' disabled'
                if 'required' in field and field['required']:
                    self.html += ' required'
                if 'step' in field and field['step']:
                    self.html += f' step="{field['step']}"'
                self.html += '>'
            if 'note' in field:
                self.html += field['note']
            self.html += '</td>\n\t\t\t</tr>'
        if sub_ok_value:
            self.html += '\n\t\t\t<tr>\n\t\t\t\t<td colspan="2" class="cnt"><input type="submit" name="ok" value="'
            self.html += sub_ok_value + '">'
        if sub_cancel_value:
            self.html += f' <input type="submit" name="cancel" value="{sub_cancel_value}">'
        if sub_ok_value or sub_cancel_value:
            self.html += '</td>\n\t\t\t</tr>'
        if tag_table:
            self.html += '\n\t\t</table>'

    def checkbox(self, name, cb_params):
        # if self.validate_cb_params(cb_params):  # Около 40 строк проверки.
        if 'tr_td' in cb_params and cb_params['tr_td']:
            if 'table' in cb_params and cb_params['table']:
                self.html += '\t\t<table>'
            self.html += '\n\t\t\t<tr>\n\t\t\t\t<td'
            if 'labelCol' in cb_params and cb_params['labelCol'] > 1:
                self.html += f' colspan="{cb_params['labelCol']}"'
            self.html += '>'
            if 'label' in cb_params and cb_params['label']:
                self.html += cb_params['label']
            self.html += '</td>\n\t\t\t\t<td>'
        self.html += f'<input type="checkbox" name="{name}" id="chb{cb_params['id']}" class="chb{cb_params['id']}"'
        if name in self.request.GET:
            self.html += ' checked'
        elif 'checked' in cb_params and cb_params['checked']:
            self.html += ' checked'
        if 'onclick' in cb_params:
            self.html += f' onclick="{cb_params['onclick']}"'
        self.html += f'><label class="lbl{cb_params['id']}" for="chb{cb_params['id']}">{cb_params['on']}</label>'
        if 'tr_td' in cb_params and cb_params['tr_td']:
            self.html += '</td>\n\t\t\t</tr>'
            if 'table' in cb_params and cb_params['table']:
                self.html += '\n\t\t</table>'

    def __str__(self):
        return self.html
