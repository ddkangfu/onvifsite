#coding: utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic import FormView
from onvifsite.form import Login
import onvif, unittest
from onvif import ONVIFCamera, ONVIFService


class Camera(FormView):
    form_class = Login
    template_name = 'login.html'
    success_url = '/thanks'

    #我想从login的form类中fetch下面四个参数，然后传到media_profile_configuration中当参数，
    # 从官网只找到了这个方法，但是不知道怎么实现。
    def form_valid(self, form):
        ip = form.cleaned_data['ip']
        port = form.cleaned_data['port']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        return HttpResponseRedirect(self.get_success_url())

    #这个就是例子中的streaming的完整例子。
    def media_profile_configuration(self):
        '''
        A media profile consists of configuration entities such as video/audio
        source configuration, video/audio encoder configuration,
        or PTZ configuration. This use case describes how to change one
        configuration entity which has been already added to the media profile.
        '''

        # Create the media service
        mycam = ONVIFCamera("192.168.0.116", 81, 'admin', '888888')
        media_service = mycam.create_media_service()

        profiles = media_service.GetProfiles()

        # Use the first profile and Profiles have at least one
        token = profiles[0]._token

        # Get all video encoder configurations
        configurations_list = media_service.GetVideoEncoderConfigurations()

        # Use the first profile and Profiles have at least one
        video_encoder_configuration = configurations_list[0]

        # Get video encoder configuration options
        options = media_service.GetVideoEncoderConfigurationOptions({'ProfileToken':token})

        # Setup stream configuration
        video_encoder_configuration.Encoding = 'H264'
        # Setup Resolution
        video_encoder_configuration.Resolution.Width = \
                        options.H264.ResolutionsAvailable[0].Width
        video_encoder_configuration.Resolution.Height = \
                        options.H264.ResolutionsAvailable[0].Height
        # Setup Quality
        video_encoder_configuration.Quality = options.QualityRange.Min
        # Setup FramRate
        video_encoder_configuration.RateControl.FrameRateLimit = \
                                        options.H264.FrameRateRange.Min
        # Setup EncodingInterval
        video_encoder_configuration.RateControl.EncodingInterval = \
                                        options.H264.EncodingIntervalRange.Min
        # Setup Bitrate
        video_encoder_configuration.RateControl.BitrateLimit = \
                                options.Extension.H264[0].BitrateRange[0].Min[0]

        # Create request type instance
        request = media_service.create_type('SetVideoEncoderConfiguration')
        request.Configuration = video_encoder_configuration
        # ForcePersistence is obsolete and should always be assumed to be True
        request.ForcePersistence = True

        # Set the video encoder configuration
        media_service.SetVideoEncoderConfiguration(request)

        # 我不知道如何返回到前端的canvas中。
        return "help"