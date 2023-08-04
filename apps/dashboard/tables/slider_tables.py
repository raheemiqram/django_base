from ajax_datatable.views import AjaxDatatableView

from apps.cms.models import Slider


class SliderAjaxDatatableView(AjaxDatatableView):
    model = Slider
    title = 'Sliders'
    initial_order = [["updated", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': False, },
        {'name': 'name', 'visible': True, },
        {'name': 'slug', 'visible': True, },
        {'name': 'created', 'visible': True},
        {'name': 'updated', 'visible': True},
        {'name': 'created_by', 'visible': True},
        {'name': 'modified_by', 'visible': True},
        {'name': 'actions', 'title': 'Actions', 'placeholder': True, 'searchable': False, 'orderable': False, },
    ]

    # {'name': 'app_label', 'foreign_field': 'content_type__app_label', 'visible': True, },

    def customize_row(self, row, obj):
        row['actions'] = """
            <a href="/dashboard/empty/" class="btn btn-info">
               Edit
            </a>
            <a href="/dashboard/empty/" class="btn btn-danger">
               Delete
            </a>
        """

    # def render_row_details(self, pk, request=None):
    #     detail = self.model.objects.get(pk=pk)
    #     html = f"""
    #     <table class="row-details">
    #     <tr>
    #     <td>First Name</td>
    #     <td>{detail.first_name}</td>
    #     </tr>
    #     <tr>
    #     <td>Last Name</td>
    #     <td>{detail.first_name}</td>
    #     </tr>
    #     <tr>
    #     <td>Email</td>
    #     <td>{detail.email}</td>
    #     </tr>
    #     </table>
    #     """
    #     return html
