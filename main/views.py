from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from .models import CustomUser,Plan,Line,Product,Transctions,WithdrawalRequest,Links,Payment
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView,View
from django.contrib.auth.mixins import LoginRequiredMixin
class HomeView(TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        # If authentication is successful, log in the user
        if user is not None:
            try:
                login(request, user)
                if user.plan is not None:
                    if user.payment_confirm:
                        return redirect('/dashboard/')
                    else:
                        return redirect('/pending/')
                else:
                    # Redirect to a success page
                    return redirect('/plans/')
            except Exception as e:
                # If an error occurs during saving, show error message
                messages.error(request, f'Error occurred: {str(e)}')

        # If authentication fails, redirect to the login page with an error message
        messages.error(request, 'Invalid email or password. Please try again.')
        return redirect('/login/')  # Adjust the URL as needed

class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        # If authentication is successful, log in the user
        if user is not None:
            try:
                login(request, user)
                if user.plan is not None:
                    if user.payment_confirm:
                        return redirect('/dashboard/')
                    else:
                        return redirect('/pending/')
                else:
                    # Redirect to a success page
                    return redirect('/plans/')
            except Exception as e:
                # If an error occurs during saving, show error message
                messages.error(request, f'Error occurred: {str(e)}')

        # If authentication fails, redirect to the login page with an error message
        messages.error(request, 'Invalid email or password. Please try again.')
        return redirect('/login/')  # Adjust the URL as needed

        # If authentication fails or form is invalid, render the login form with errors


from django.contrib import messages
from django.views.generic import TemplateView
from .models import CustomUser

class RegisterView(TemplateView):
    template_name = 'signup.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            # Get form data from POST request
            first_name = request.POST.get('firstName')
            last_name = request.POST.get('lastName')
            email = request.POST.get('email')
            mobile = request.POST.get('phoneNumber')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            # Check if passwords match
            if password != password2:
                # If passwords don't match, show error message
                messages.error(request, 'Passwords do not match.')
                return super().get(request, *args, **kwargs)

            # Check if all required fields are present
            if not all([first_name, last_name, email, mobile, password]):
                # If any required field is missing, show error message
                messages.error(request, 'All fields are required.')
            else:
                try:
                    # Create a new CustomUser instance and save it to the database
                    user = CustomUser.objects.create_user(email=email, first_name=first_name, last_name=last_name, mobile=mobile, password=password)
                    # Optionally, add success message
                    messages.success(request, 'User registered successfully.')
                except Exception as e:
                    # If an error occurs during saving, show error message
                    messages.error(request, f'Error occurred: {str(e)}')

        else:
            # If request method is not POST, show error message
            messages.error(request, 'Invalid request method.')

        # Redirect back to the same page or to a different page
        return redirect('/login/')
        return super().get(request, *args, **kwargs)
from django.urls import reverse

class PlansView(TemplateView):
    template_name = 'Plans.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plans'] = Plan.objects.all()
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # User is not logged in, redirect to the login page
            return redirect(reverse('login'))  # Replace 'login' with the name of your login URL pattern
        return super().dispatch(request, *args, **kwargs)

from urllib.parse import unquote
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import Plan
from django.http import HttpResponseBadRequest
class PaymentView(TemplateView):
    template_name = 'rtx.html'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # User is not logged in, redirect to the login page
            return redirect(reverse('login'))  # Replace 'login' with the name of your login URL pattern
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logged_in_user = request.user
        print(logged_in_user)

        # Get the plan name from URL kwargs
        encoded_plan_name = self.kwargs.get('plan')

        # Decode the URL-encoded plan name
        plan_name = unquote(encoded_plan_name)

        try:
            # Query the Plan model to find a plan with a similar name
            plan = Plan.objects.get(url__iexact=plan_name)
            print(plan)
        except Plan.DoesNotExist:
            # If no plan matches the name, raise a 404 error
            raise Http404("Plan does not exist")

        # Print the matched plan in the console
        print(f"Plan: {plan}")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        number = Payment.objects.get(id=1)  # Adjust this query as needed
        context["number"] = number.number
        return context

    def post(self, request, *args, **kwargs):
        logged_in_user = request.user
        print(logged_in_user)
        if 'TRX' not in request.POST:
            return HttpResponseBadRequest("No TRX ID Given uploaded")
        # Get the plan name from URL kwargs
        encoded_plan_name = self.kwargs.get('plan')

        # Decode the URL-encoded plan name
        plan_name = unquote(encoded_plan_name)

        try:
            # Query the Plan model to find a plan with a similar name
            plan = Plan.objects.get(url__iexact=plan_name)
            TRX = request.POST.get('TRX')

            # Update the trx_id field of the logged-in user
            logged_in_user.trx_id = TRX
            logged_in_user.plan = plan
            logged_in_user.save()

            print(plan)
        except Plan.DoesNotExist:
            # If no plan matches the name, raise a 404 error
            raise Http404("Plan does not exist")

        # Print the matched plan in the console
        print(f"Plan: {plan}")
        return redirect('/pending/')
        # Call the parent class's get method to handle rendering the template
        return super().get(request, *args, **kwargs)


class PaymentPendingView(TemplateView):
    template_name = 'paymentpending.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # User is not logged in, redirect to the login page
            return redirect(reverse('login'))  # Replace 'login' with the name of your login URL pattern
        return super().dispatch(request, *args, **kwargs)

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # User is not logged in, redirect to the login page
            return redirect(reverse('login'))  # Replace 'login' with the name of your login URL pattern
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logged_in_user = request.user
        print(logged_in_user)
        if logged_in_user.payment_confirm:
            # Render the dashboard template if the user's payment is confirmed
            data = Line.objects.all()  # Assuming Line is your model
            top_users = CustomUser.objects.filter(on_dashboard=True)
            return render(request, self.template_name, context={'lines': data,'top_users': top_users})
        else:
            # Redirect to the pending payment page if the user's payment is not confirmed
            return redirect('/pending/')


class Rate(TemplateView):
    template_name = 'rate.html'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # User is not logged in, redirect to the login page
            return redirect(reverse('login'))  # Replace 'login' with the name of your login URL pattern
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        logged_in_user = self.request.user
        print(logged_in_user)
        id = self.kwargs.get('id')
        product = logged_in_user.products.get(id=id)
        return render(request,self.template_name,context={'product':product})
    def post(self, request, *args, **kwargs):
        logged_in_user = self.request.user
        id = self.kwargs.get('id')

        try:
            product = logged_in_user.products.get(id=id)
        except Product.DoesNotExist:
            messages.error(request, "Product does not exist.")
            return HttpResponseRedirect(reverse('rate'))

        rate = request.POST.get('rating')
        if int(rate) < 5:
            messages.error(request, "Please rate 5 stars.")
            return HttpResponseRedirect(reverse('rate', kwargs={'id': id}))
        else:
            print(rate)
            if product.rating < 5:
                print(logged_in_user.Balance)
                print(logged_in_user.plan.per_product_earning)
                print(logged_in_user.plan)
                logged_in_user.Balance +=  logged_in_user.plan.per_product_earning
                logged_in_user.save()
                product.rating = rate
                product.save()
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                return redirect(f'/rate/{id}/',context={messages.error(request, "Product Aready Rated")})
class WorkView(TemplateView):
    template_name = 'work.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        products = user.products.all()  # Retrieve all products associated with the user
        context["products"] = products
        return context


class Profile(TemplateView):
    template_name = 'profile.html'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # User is not logged in, redirect to the login page
            return redirect(reverse('login'))  # Replace 'login' with the name of your login URL pattern
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.request.user.id
        user = self.request.user
        print(user)
        Payments = user.transctions.all()
        context["userData"] = CustomUser.objects.get(id=id)
        context["Transctions"] = Payments
        return context

    def post(self, request, *args, **kwargs):
        # Handle the form submission
        image_file = request.FILES.get('image1')  # 'image1' should match the name attribute of your file input
        if image_file:
            # Save the uploaded image to the user's profile
            user = request.user
            user.image = image_file
            user.save()
            # Optionally, redirect the user to a success page or back to the profile page
            return redirect('profile')  # Replace 'profile' with the name of your profile URL pattern
        else:
            # Handle the case where no image is uploaded
            # You can render the profile page again with an error message, if needed
            return render(request, self.template_name, {'error_message': 'No image uploaded.'})

class Wallet(TemplateView):
    template_name = 'payMethod.html'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # User is not logged in, redirect to the login page
            return redirect(reverse('login'))  # Replace 'login' with the name of your login URL pattern
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        Payments = user.transctions.all()
        context["Transctions"] = Payments
        context["Amount"] = user.Balance
        context["Reward"] =  user.reward_earning
        context["level"] = user.rank_level
        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user
        email = request.POST.get('email')
        account_name = request.POST.get('name')
        account_number = request.POST.get('mobile')
        billing_state = request.POST.get('platform')
        amount = request.POST.get('amount')

        print(account_name)
    # Save the data to the WithdrawalRequest model
        withdrawal_request = WithdrawalRequest.objects.create(
            email=email,
            account_name=account_name,
            amount=amount,
            account_number=account_number,
            billing_state=billing_state,
        )

    # Add the created withdrawal request to the user's withdrawalrequests
        user.withdrawalrequests.add(withdrawal_request)

        # Redirect to a success page or any other page
        return redirect('/dashboard/')


class TeamView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # User is not logged in, redirect to the login page
            return redirect(reverse('login'))  # Replace 'login' with the name of your login URL pattern
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        link = self.request.user.invite_link
        teams = self.request.user.referrals.all()
        context["link"] = link
        context["teams"] = teams
        return context

    template_name = 'teams.html'


class ReferView(TemplateView):
    template_name = 'signup.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            # Get form data from POST request
            first_name = request.POST.get('firstName')
            last_name = request.POST.get('lastName')
            email = request.POST.get('email')
            mobile = request.POST.get('phoneNumber')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            invite = kwargs.get('invite')

            # Check if passwords match
            if password != password2:
                # If passwords don't match, show error message
                messages.error(request, 'Passwords do not match.')
                return redirect('/signup/refer/', slug=invite)

            # Check if all required fields are present
            if not all([first_name, last_name, email, mobile, password]):
                # If any required field is missing, show error message
                messages.error(request, 'All fields are required.')
                return redirect('/signup/refer/', slug=invite)

            try:
                # Find the referrer user based on the invite link
                referrer = CustomUser.objects.get(invite_link=invite)
                if referrer.plan.id == 1:
                    referrer.Balance += 150
                    referrer.save()
                elif referrer.plan.id ==2:
                    referrer.Balance += 275
                    referrer.save()
                elif referrer.plan.id == 3:
                    referrer.Balance += 580
                    referrer.save()
                elif referrer.plan.id == 4:
                    referrer.Balance += 1150
                    referrer.save()
                else:
                    referrer.Balance += 0
                    referrer.save()
                # Create a new CustomUser instance and save it to the database
                user = CustomUser.objects.create_user(email=email, first_name=first_name, last_name=last_name, mobile=mobile, password=password)

                # Add the new user to the referrer's list of referrers
                referrer.referrals.add(user)

                # Optionally, add success message
                messages.success(request, 'User registered successfully.')

            except CustomUser.DoesNotExist:
                # If the referrer user does not exist, show error message
                messages.error(request, 'Invalid referral link.')
                return redirect('/signup/refer/', slug=invite)

            except Exception as e:
                # If an error occurs during saving, show error message
                messages.error(request, f'Error occurred: {str(e)}')
                return redirect('/signup/refer/', slug=invite)

            # Redirect to login page
            return redirect('/login/')

        else:
            # If request method is not POST, show error message
            messages.error(request, 'Invalid request method.')

        # Redirect back to the same page or to a different page
        return redirect('signup/refer/', slug=invite)


class RewardView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # User is not logged in, redirect to the login page
            return redirect(reverse('login'))  # Replace 'login' with the name of your login URL pattern
        return super().dispatch(request, *args, **kwargs)
    template_name = "ranking.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get rank level of the current user
        rank = self.request.user.rank_level
        link = self.request.user.invite_link
        # Define the number of referrals needed for each rank level
        rank_levels = [
            (5, 2),    # On 5 members Rank 2
            (15, 3),   # On 15 members Rank 3
            (40, 4),   # On 40 members Rank 4
            (65, 5),   # On 65 members Rank 5
            (100, 6),  # On 100 members Rank 6
            (140, 7),  # On 140 members Rank 7
            (190, 8),  # On 190 members Rank 8
            (260, 9),  # On 260 members Rank 9
            (780, 10)  # On 780 members Rank 10
        ]

        # Find the next rank level and the number of referrals needed for the next rank
        next_rank, referrals_needed = None, None
        for referrals, level in rank_levels:
            if rank < level:
                next_rank, referrals_needed = level, referrals
                break

        # Calculate the progress percentage for the current rank
        referral_count = self.request.user.referrals.count()
        progress_percentage = (referral_count / referrals_needed) * 100 if referrals_needed else 0

        # Calculate the progress percentage for the next rank
        next_progress_percentage = ((referral_count + 1) / referrals_needed) * 100 if referrals_needed else 0
        links = self.request.user.links.all()
        # Pass data to the context
        print(links)
        context["current_rank"] = rank
        context["next_rank"] = next_rank
        context["referrals_needed"] = referrals_needed
        context["progress_percentage"] = progress_percentage
        context["next_progress_percentage"] = next_progress_percentage
        context["link"] = link
        context["links"] = links
        return context

class LinkClickView(LoginRequiredMixin, View):
    def get(self, request, link_id, *args, **kwargs):
        # Ensure the user is logged in
        if not request.user.is_authenticated:
            return HttpResponse('<h1>You must be logged in to access this page</h1>')

        # Retrieve the current user
        user = request.user

        # Validate the link_id
        if link_id not in [1, 2, 3, 4]:
            return HttpResponse('<h1>Invalid link ID</h1>')

        # Determine which link was clicked based on the link_id parameter
        link_attr = f'click_on_link{link_id}'
        if not getattr(user, link_attr, False):
            # Update the click_on_link attribute and balance
            setattr(user, link_attr, True)
            user.reward_earning += user.plan.link_earning
            user.save()
        else:
            return HttpResponse(f'<h1>Already clicked on link {link_id} today</h1>')

        # Get the link object based on the link_id
        link = get_object_or_404(Links, id=link_id)

        # Redirect the user to the destination URL
        return redirect(link.url)
