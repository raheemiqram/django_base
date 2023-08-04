from ajax_datatable.views import AjaxDatatableView
from apps.users.models import User


class UserAjaxDatatableView(AjaxDatatableView):
    model = User
    title = 'Users'
    initial_order = [["email", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': False, },
        {'name': 'first_name', 'visible': True, },
        {'name': 'last_name', 'visible': True, },
        {'name': 'email', 'visible': True},
        {'name': 'is_staff', 'visible': True},
        {'name': 'actions', 'title': 'Actions', 'placeholder': True, 'searchable': False, 'orderable': False, },
    ]

    # {'name': 'app_label', 'foreign_field': 'content_type__app_label', 'visible': True, },

    def customize_row(self, row, obj):
        row['actions'] = """
            <a href="/dashboard/empty/" class="btn btn-info">
               Edit
            </a>
            <a href="/dashboard/empty/" class="btn btn-danger">
               Edit
            </a>
        """

    def render_row_details(self, pk, request=None):
        detail = self.model.objects.get(pk=pk)
        html = f"""
        <table class="row-details">
        <tr>
        <td>First Name</td>
        <td>{detail.first_name}</td>
        </tr>
        <tr>
        <td>Last Name</td>
        <td>{detail.first_name}</td>
        </tr>
        <tr>
        <td>Email</td>
        <td>{detail.email}</td>
        </tr>
        </table>
        """
        return html
