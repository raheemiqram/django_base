from allauth.account.adapter import DefaultAccountAdapter as BaseDefaultAccountAdapter


class DefaultAccountAdapter(BaseDefaultAccountAdapter):

    def send_mail(self, template_prefix, email, context):
        msg = self.render_mail(template_prefix, email, context)
        try:
            msg.send()
        except Exception as e:
            # Todo: need to handle exception
            pass
