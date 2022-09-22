
from django import forms

class EdaDropdownForm(forms.Form):
    id_col = forms.CharField(label='id_col', max_length=100)
    target_col = forms.CharField(label='target_col', max_length=100)
    time_index_col = forms.CharField(label='time_index_col', max_length=100)
    static_cat_col_list = forms.CharField(label='static_cat_col_list', max_length=100)
    static_num_col_list = forms.CharField(label='static_num_col_list', max_length=100)
    temporal_known_num_col_list = forms.CharField(label='temporal_known_num_col_list', max_length=100)
    temporal_known_cat_col_list = forms.CharField(label='temporal_known_cat_col_list', max_length=100)
    sort_col_list = forms.CharField(label='sort_col_list', max_length=100)



# 'id_col': 'cpf',
# 'target_col': 'PHY_CS',
# 'time_index_col': 'G_WEEK',
# 'static_num_col_list': [],
# 'static_cat_col_list': ['BrandCode'],
# 'temporal_known_num_col_list':  ['Product_discount'],
# 'temporal_unknown_num_col_list': [],
# 'temporal_known_cat_col_list': ['M'],
# 'temporal_unknown_cat_col_list': [],
# 'strata_col_list': [],
# 'sort_col_list': ['cpf'],
# 'wt_col': None