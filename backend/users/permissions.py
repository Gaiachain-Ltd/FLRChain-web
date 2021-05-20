from rest_framework.permissions import BasePermission
from users.models import CustomUser


class isBeneficiary(BasePermission):
    def has_permission(self, request, view):
        return request.user.type == CustomUser.BENEFICIARY


class isFacilitator(BasePermission):
    def has_permission(self, request, view):
        return request.user.type == CustomUser.FACILITATOR

    
class isInvestor(BasePermission):
    def has_permission(self, request, view):
        return request.user.type == CustomUser.INVESTOR


class isOptedIn(BasePermission):
    def has_permission(self, request, view):
        return request.user.opted_in