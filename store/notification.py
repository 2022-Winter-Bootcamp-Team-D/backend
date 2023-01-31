import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
class notify:
    cred = credentials.Certificate('./store/service_account.json')
    default_app = firebase_admin.initialize_app(cred)

    def enter_notify(token):
        """
        매장에서 호출할 경우 알림 보내기 1인에게 감
        """
        # See documentation on defining a message payload.
        message = messaging.Message(
            android=messaging.AndroidConfig(
                priority='normal',
                notification=messaging.AndroidNotification(
                    title='입장 알림',
                    body='고객님! 매장으로 입장해주세요!',
                    icon='',
                    sticky='false',  # 알람 기능 입장 알림에 넣으면 좋을 듯
                    sound='default'
                ),
            ),
            token=token
        )

        # Send a message to the device corresponding to the provided
        response = messaging.send(message)
        # Response is a message ID string.
        return response

    def auto_notify(token):
        """
        매장에 대기 팀이 입장했을 경우 대기 1순위 팀에게 알림
        result = notify.enter_notify(token)
        tokens => 대기 1순위 토큰
        """
        message = messaging.Message(
            android=messaging.AndroidConfig(
                priority='normal',
                notification=messaging.AndroidNotification(
                    title='대기 순서 알림',
                    body='현재 대기 1순위 입니다! 매장 앞에서 대기해 주세요.',
                    icon='',
                    sound='default'
                ),
            ),
            token=token
        )
        response = messaging.send(message)
        return response

    def cancel_notify(token):
        """
        팀이 취소하거나 취소 당할 경우
        result = notify.cancel_notify(token)
        tokens => 취소자 토큰
        """
        message = messaging.Message(
            android=messaging.AndroidConfig(
                priority='normal',
                notification=messaging.AndroidNotification(
                    title='대기 취소 알림',
                    body='웨이팅이 취소되었습니다.',
                    icon='',
                    sound='default'
                ),
            ),
            token=token
        )
        response = messaging.send(message)
        return response
