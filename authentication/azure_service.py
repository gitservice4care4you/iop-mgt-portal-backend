import http.client
import os
import jwt
import requests
from jwt.algorithms import RSAAlgorithm
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
import http


class AzureService:
    USER_PROFILE_MS_GRAPH_API = "https://graph.microsoft.com/v1.0/me/"

    def __init__(
        self,
    ) -> None:
        pass

    def get_user_profile(self, azure_access_token):
        """
        Fetches user profile from Microsoft Graph API using the provided Azure access token.

        Args:
            azure_access_token (str): The Azure access token to authenticate the request

        Returns:
            dict: The user profile data from Microsoft Graph API
        """
        try:
            headers = {
                "Authorization": f"Bearer {azure_access_token}",
                "Content-Type": "application/json",
            }

            response = requests.get(self.USER_PROFILE_MS_GRAPH_API, headers=headers)

            # Raise an exception for HTTP errors
            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as e:
            # Handle request errors
            return {"error": str(e)}

    def get_user_from_json(self, azure_user):
        azure_id = azure_user.get("id")
        email = (
            str(azure_user.get("mail")).lower()
            or str(azure_user.get("userPrincipalName")).lower()
        )
        first_name = azure_user.get("givenName")
        last_name = azure_user.get("surname")
        full_name = azure_user.get("displayName")
        job_title = azure_user.get("jobTitle")
        country_code = azure_user.get("officeLocation")

        if country_code:
            # Try to get country object from database using the country code
            country = self._get_country(country_code=country_code)
        # Prepare user data dictionary
        user_data = {
            "azure_id": azure_id,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "full_name": full_name,
            "job_title": job_title,
            "country": country_code if country_code else None,
        }

        return user_data

    def get_user_photo(self, azure_access_token):
        """
        Fetches user photo from Microsoft Graph API using the provided Azure access token.

        Args:
            azure_access_token (str): The Azure access token to authenticate the request

        Returns:
            str: The URL of the user's photo
        """
        try:
            headers = {
                "Authorization": f"Bearer {azure_access_token}",
                "Content-Type": "application/json",
            }

            response = requests.get(
                self.USER_PROFILE_MS_GRAPH_API + "photo/$value", headers=headers
            )
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            return None

    def _get_country(self, country_code):
        try:
            from country.models import Country

            country_obj = Country.objects.filter(code__iexact=country).first()
            if country_obj:
                country = country_obj
            # If country not found by code, try to find by name
            else:
                country_obj = Country.objects.filter(name__iexact=country).first()
                if country_obj:
                    country = country_obj
        except Exception as e:
            # If there's an error retrieving the country, keep the original string value
            pass

    # def _decode_azure_token(self, azure_token):
    #     """
    #     Decodes the Azure access token using the public key from the Microsoft Graph API.

    #     Args:
    #         azure_token (str): The Azure access token to decode
    #     """
    #     try:
    #         # Get the public key from the Microsoft Graph API
    #         response = requests.get(self.USER_PROFILE_MS_GRAPH_API + "/.well-known/openid-configuration")
    #         response.raise_for_status()
    #         openid_config = response.json()
    #         jwks_uri = openid_config.get("jwks_uri")

    #         # Get the public key from the JWKS endpoint
    #         response = requests.get(jwks_uri)
    #         response.raise_for_status()
    #         jwks = response.json()

    #         # Decode the token
    #         decoded_token = jwt.decode(
    #             azure_token,
    #             jwks,
    #             algorithms=["RS256"],
    #         )
    #         return decoded_token
    #     except Exception as e:
    #         return None
