from django.urls import path
from builds.views import BuildDetailView,BuildBuildView,BuildUpdateView,BuildDeleteView

app_name = 'builds'

urlpatterns = [
    #path("", BuildListView.as_view(), name="build_list"),
    path("<int:profile_id>/", BuildDetailView.as_view(), name="build_detail"),
    path('<int:profile_id>/build/', BuildBuildView.as_view(), name='build_build'),
    path('<int:profile_id>/update/', BuildUpdateView.as_view(), name='build_update'),
    path('<int:profile_id>/delete/', BuildDeleteView.as_view(), name='build_delete'),
]
