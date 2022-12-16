from django.contrib.auth.tokens import default_token_generator

confirmation_code = default_token_generator.make_token(user)