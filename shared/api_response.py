from rest_framework.response import Response


class APIResponse(Response):

    @classmethod
    def success(cls, message: str, status_code: int, data: any = None):
        # print("data", data)
        res_data = data if data != None else None
        print("res_data", res_data)
        if res_data == None:
            return Response(
                status=status_code,
                data={
                    "success": True,
                    "message": message,
                },
            )
        return Response(
            status=status_code,
            data={
                "success": True,
                "message": message,
                "data": res_data,
            },
        )

    @classmethod
    def error(cls, message, status_code):
        return Response(
            status=status_code,
            data={
                "success": False,
                "message": message,
            },
        )
