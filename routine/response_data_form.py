from enum import Enum


class ResponseStatusEnum(Enum):
    DELETE_OK = "ROUTINE_DELETE_OK"
    LIST_OK = "ROUTINE_LIST_OK"
    UPDATE_OK = "ROUTINE_UPDATE_OK"
    DETAIL_OK = "ROUTINE_DETAIL_OK"
    CREATE_OK = "ROUTINE_CREATE_OK"


class ResponseMessageEnum(Enum):
    MSG_DELETE = "루틴 삭제 성공"
    MSG_CREATE = "루틴 생성 성공"
    MSG_DETAIL = "루틴 조회 성공"
    MSG_LIST = "루틴 조회 성공"
    MSG_UPDATE = "루틴 수정 성공"


class ResponseDataForm(object):
    __default_form = {
                "data": {

                },
                "message": {
                    "msg": "", "status": ""
                }
            }

    def __init__(self, status: ResponseStatusEnum, msg: ResponseMessageEnum):
        self.status = status
        self.msg = msg

    def get_response_form(self):
        default_form = self.__default_form
        default_form['message']['msg'] = self.msg.value
        default_form['message']['status'] = self.status.value
        return default_form
