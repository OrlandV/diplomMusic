from django import forms
# from .fields import *


class OMSForm(forms.Form):
    chbSort = forms.BooleanField(
        label='↓',
        label_suffix='',
        required=False,
        widget=forms.CheckboxInput({'auto_id': False, 'id': 'chbSort', 'class': 'chbSort'})
    )


class RppForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs['auto_id'] = False
        super().__init__(*args, **kwargs)

    rpp = forms.IntegerField(label='Количество отображаемых записей на странице:', initial=10, max_value=100,
                             min_value=1, step_size=1)


# class OMSForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         kwargs['auto_id'] = False
#         kwargs['label_suffix'] = ''
#         super().__init__(*args, **kwargs)
#
#     sort_dict = {None: ''}
#     sort_dict.update({f[0]: f[1] for f in cur_fields(list(range(13)))})
#     selSort = forms.ChoiceField(
#         choices=sort_dict,
#         label='',
#         required=False,)
#     selSort.widget.attrs.update({'id': 'selSort', 'data-change': 'selSort'})
#     chbSort = forms.BooleanField(
#         label='↓',
#         required=False,
#         widget=forms.CheckboxInput({'id': 'chbSort', 'class': 'chbSort'})
#     )


# class SearchForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         kwargs['auto_id'] = False
#         super().__init__(*args, **kwargs)
#
#     # <select name="perfo[]" id="perfo[]" multiple size="6">
#     perfo = forms.MultipleChoiceField()
#     # <input type="text" name="namor" size="100" value=""> <span class="font80">(до 100 символов)</span>
#     namor = forms.CharField(max_length=fields()[2][3], required=False)  # max_length=100
#     # <input type="text" name="namro" size="100" value=""> <span class="font80">(до 100 символов)</span>
#     namro = forms.CharField(max_length=fields()[3][3], required=False)  # max_length=100
#     # <input type="text" name="namen" size="100" value=""> <span class="font80">(до 100 символов)</span>
#     namen = forms.CharField(max_length=fields()[4][3], required=False)  # max_length=100
#     # <select name="album" id="album">
#     album = forms.ChoiceField()
#     # <input type="time" name="trdur" value="" step="1">
#     trdur = forms.TimeField()
#     # <select name="lyric[]" id="lyric[]" multiple size="6">
#     lyric = forms.MultipleChoiceField()
#     # <select name="compo[]" id="compo[]" multiple size="6">
#     compo = forms.MultipleChoiceField()
#     # <select name="arran[]" id="arran[]" multiple size="6">
#     arran = forms.MultipleChoiceField()
#     # <select name="ostfr[]" id="ostfr[]" multiple size="6">
#     ostfr = forms.MultipleChoiceField()
#     # <input type="text" name="notes" size="200" value=""> <span class="font80">(до 380 символов)</span>
#     notes = forms.CharField(max_length=fields()[12][3], required=False)  # max_length=380
#     # Строгий режим&nbsp;&nbsp;<img src="/img/quest.png" width="18" height="18" class="help-head" onclick="helpClick('help-body');">
#     # <input type="checkbox" name="chbStr" id="chbStr" class="chbStr"><label class="lblStr" for="chbStr">Да</label>
#     chbStr = forms.BooleanField(
#         # label='Да',
#         # required=False,
#         # widget=forms.CheckboxInput({'id': 'chbStr', 'class': 'chbStr'})
#     )
