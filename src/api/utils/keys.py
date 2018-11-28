import os
class Keys:
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    AWS_COGNITO_CLIENT_ID = os.environ.get('AWS_COGNITO_CLIENT_ID')
    AWS_COGNITO_USERPOOL_ID = os.environ.get('AWS_COGNITO_USERPOOL_ID')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    STRIPE_PUBLISH_KEY = os.environ.get('STRIPE_PUBLISH_KEY')
