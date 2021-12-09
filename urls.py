from django.urls import path
from . import log_views,home_views,graphs_views
from main.Dash_apps.Apps import graphs, graphs2

urlpatterns = [

path("",log_views.loginPage, name="login"),
path("sign_up/", log_views.sign, name="sign"),
path("login/", log_views.loginPage, name="login"),
path("welcome_new_user/", log_views.welcome, name="welcome"),
path("fail_email_validation/", log_views.fail_email_validation, name="fail_email_validation"),
path("logout/", log_views.logoutPage, name="logout"),

path("home/", home_views.home, name="home"),
path("flat/", home_views.flat, name="flat"),
path("food/", home_views.food, name="food"),
path("others/", home_views.others, name="others"),
path("school/", home_views.school, name="school"),
path("settings/", home_views.settings, name="settings"),

path("wallet/", graphs_views.wallet, name="wallet"),
path("graphs/", graphs_views.graphs, name="graphs"),

path("dash_plot/",graphs_views.dash_plot, name="dash_plot"),
]