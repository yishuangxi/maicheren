# coding:utf8
import os

app_config = dict(
  gzip=True,
  debug=True,
  cookie_secret="yIFr7VYAxmipCxZFaIK3YyMYZxFHEB7LOW1SFe6cI",
  # xsrf_cookies=True,
  template_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'front/src'),
  static_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'front/src/static'),
)
