from users.models import user_designations
from allauth.socialaccount.models import SocialAccount


class designationsToBeInvolve:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)

        return response

    def process_view(self, request, view_func, *view_args, **view_kargs):
        if request.user.is_authenticated:

            request.role=None
            users = request.user
            prov = SocialAccount.objects.filter(user_id=users)
            if len(prov)>0:
                if prov[0].provider=='google':
                    obj=user_designations.objects.filter(user=users)
                    if len(obj) == 0:
                        create_user = user_designations.objects.create(user=users, designations='user')
                        create_user.save()

            role = request.user.user_designations.designations
            if role:
                request.role = role

