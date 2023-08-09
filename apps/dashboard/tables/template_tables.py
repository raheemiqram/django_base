from ajax_datatable.views import AjaxDatatableView
from apps.messaging.models import Template


class TemplateAjaxDatatableView(AjaxDatatableView):
    model = Template
    title = 'Template'
    initial_order = [["updated", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': False, },
        {'name': 'title', 'visible': True, },
        {'name': 'template_type', 'visible': True, },
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
            <a href="#" class="btn btn-danger" data-toggle="modal" data-target="#modal-default_{pk}">
               Delete
            </a>
            
            <div class="modal fade" id="modal-default_{pk}" style="display: none;" aria-hidden="true">
                <div class="modal-dialog">
                <div class="modal-content">
                <div class="modal-header">
                <h4 class="modal-title">Default Modal</h4>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">×</span>
                </button>
                </div>
                <div class="modal-body">
                <p>One fine body…</p>
                </div>
                <div class="modal-footer justify-content-between">
                <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary">Save changes</button>
                </div>
                </div>
                </div>
            </div>
        """.format(pk=obj.id)

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
