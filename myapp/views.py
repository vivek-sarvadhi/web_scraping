from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
import requests
from bs4 import BeautifulSoup
import re
# Create your views here.
class IndexAPIView(ListAPIView):

    def get(self, request, *args, **kwargs):
        return Response(data={'status':status.HTTP_202_ACCEPTED, 'Message':'Hello world!'},status=status.HTTP_202_ACCEPTED)


class WebScrapeAPIView(GenericAPIView):

    def get(self, request):
        try:
            url = self.request.query_params.get('url')
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
            response = requests.get(url, headers=headers)
            htmlContent = response.content
            soup = BeautifulSoup(htmlContent, 'html.parser')
            header = soup.find("header", class_="up-card-header d-flex").get_text()
            job_breadcrumb = soup.find('div', {'class': 'cfe-ui-job-breadcrumbs d-inline-block mr-10'}).get_text()
            job_link = soup.find('div', {'class': 'cfe-ui-job-breadcrumbs d-inline-block mr-10'})
            posted_on = soup.find('div', {'id': 'posted-on'}).get_text()
            location_restrication = soup.find('div', {'class': 'mt-20 d-flex align-items-center location-restriction'}).get_text()
            job_link_url = job_link.a['href']
            content = soup.find("div", class_="job-description").get_text()

            job_features = soup.find('ul', {'class': 'cfe-ui-job-features p-0 fluid-layout-md'}).findAll("li", recursive=False)
            jobfeaturedetail = []
            for job_feature in job_features:
                jobfeaturedetail.append(job_feature.stripped_strings)
            jobfeature_dict = {}
            for i in jobfeaturedetail:
                key1 = ""
                value1 = ""
                for id,line in enumerate(i):
                    if id == 1:
                        key = line
                        if key.startswith('-$'):
                            key1 = key
                            key = "Hourly Rate"
                    else:
                        value = line
                        if value.startswith('$'):
                            value1 = value
                    new_value = value1 + key1
                    if value == "Hourly":
                        value = new_value
                for jobfeature_key in jobfeature_dict.keys():
                    if jobfeature_key == key:
                        key = "location"
                jobfeature_dict[key] = value


            skills = soup.find(class_="fluid-layout").findAll("div", recursive=False)
            skilldetail = []
            for skill in skills:
                skilldetail.append(skill.stripped_strings)
            skills_dict = {}
            for i in skilldetail:
                value_list = []
                for id,line in enumerate(i):
                    if id == 0:
                        key = line
                    else:
                        value = line
                        value_list.append(value)
                skills_dict[key] = value_list


            activitys = soup.find("ul", class_="list-unstyled mb-0").findAll("li", recursive=False)
            activitydetail = []
            for activity in activitys:
                activitydetail.append(activity.stripped_strings)
            activity_dict = {}
            for i in activitydetail:
                activity_list = []
                for id,line in enumerate(i):
                    if id == 1:
                        key = line
                    else:
                        value = line
                        activity_list.append(value)
                activity_dict[key] = activity_list


            client_location = soup.find('li', {'data-qa': 'client-location'}).get_text()
            client_job_posting_state = soup.find('li', {'data-qa': 'client-job-posting-stats'}).get_text()
            client_company_profile = soup.find('li', {'data-qa': 'client-company-profile'}).get_text()
            client_contract_date = soup.find('li', {'data-qa': 'client-contract-date'}).get_text()
            client_spend = soup.find('strong', {'data-qa': 'client-spend'})
            client_hires = soup.find('div', {'data-qa': 'client-hires'})
            client_hourly_rate = soup.find('strong', {'data-qa': 'client-hourly-rate'})
            client_hours = soup.find('div', {'data-qa': 'client-hours'})
            client_hire_spend = ""
            client_rate_hourly = ""
            if client_spend or client_hires is not None:
                client_hire_spend = client_spend.stripped_strings, client_hires.stripped_strings
            if client_hourly_rate or client_hours is not None:
                client_rate_hourly = client_hourly_rate.stripped_strings, client_hours.stripped_strings

            return Response(data={"status": status.HTTP_200_OK,
                                "message": "display data",
                                "data": {"Header":header,
                                        "Job Detail":{
                                            "Search more":[job_breadcrumb,job_link_url],
                                            "jobs":posted_on,
                                            "Location":location_restrication
                                        },
                                        "Content":content,
                                        "Job Features":jobfeature_dict,
                                        "Skills and Expertise": skills_dict,
                                        # "Activity on this": activity_dict,
                                        "About the client": {
                                            "client_location":client_location,
                                            "client_job_posting_state":client_job_posting_state,
                                            "client_company_profile":client_company_profile,
                                            "client_contract_date":client_contract_date,
                                            "client_hire_spend":client_hire_spend,
                                            "client_rate_hourly":client_rate_hourly

                                        },
                                    }
                                },status=status.HTTP_200_OK)
        except:
            return Response(data={'status':status.HTTP_400_BAD_REQUEST, 
                                    'Message':'Please Provide Valid Upwork website url',
                                    },status=status.HTTP_400_BAD_REQUEST)


class WebScrapeFreelancerAPIView(GenericAPIView):

    def get(self, request):
        try:
            url = self.request.query_params.get('url')
            response = requests.get(url)
            htmlContent = response.content
            soup = BeautifulSoup(htmlContent, 'html.parser')
            header = soup.find("h1", class_="PageProjectViewLogout-header-title").get_text()
            budget = soup.find("p", class_="PageProjectViewLogout-header-byLine").get_text()

            contents = soup.find("div", class_="PageProjectViewLogout-detail").findAll("p", recursive=False)
            contentdetail = []
            for content in contents[0]:
                contentdetail.append(content.stripped_strings)
            content_dict = []
            for i in contentdetail:
                for id,j in enumerate(i):
                    content_dict.append(j)
            skilldetail = []
            for content in contents[1:]:
                skilldetail.append(content.stripped_strings)
            skill_dict = {}
            for i in skilldetail:
                value_list = []
                for id,j in enumerate(i):
                    if id == 0:
                        key = j
                    else:
                        if j != ",":
                            value = j
                            value_list.append(value)
                skill_dict[key] = value_list

            employer_abouts = soup.find("div", class_="PageProjectViewLogout-detail-reputation PageProjectViewLogout-detail-tags").findAll("span", recursive=False)
            employeraboutdetail = []
            for employer_about in employer_abouts:
                employeraboutdetail.append(employer_about.stripped_strings)
            rating_review = soup.find("span", class_="Rating-review").get_text()
            client_location = soup.find("span", {'itemprop': 'addressLocality'}).get_text()
            return Response(data={'status':status.HTTP_200_OK, 
                                    'Message':'Display Freelancer Data',
                                    "data": {
                                        "Header":header,
                                        "Budget":budget,
                                        "Content":content_dict,
                                        "Project Detail":skill_dict,
                                        "Employer Detail":{
                                                "rating_review":rating_review,
                                                "client_location":client_location
                                                },
                                        },
                                    },status=status.HTTP_200_OK)
        except:
            return Response(data={'status':status.HTTP_400_BAD_REQUEST, 
                                    'Message':'Please Provide Valid Freelancer website url',
                                    },status=status.HTTP_400_BAD_REQUEST)