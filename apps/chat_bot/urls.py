from django.urls import path
from .views import NLPTaskView, CVTaskView, GMTaskView, NLTKTrainView, NLTKChatView

urlpatterns = [
    # OPEN AI
    path('nlp/', NLPTaskView.as_view(), name='chat_bot_nlp'),
    path('cv/', CVTaskView.as_view(), name='chat_bot_cv'),
    path('gm/', GMTaskView.as_view(), name='chat_bot_gm'),

    # NLTK
    path('nltk/train/', NLTKTrainView.as_view(), name='nltk_train'),
    path('nltk/chat/', NLTKChatView.as_view(), name='nltk_chat'),

]
