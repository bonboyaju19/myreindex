import logger
from enum import Enum
import sys

logger = logger.get_logger()


class ErrorType(Enum):
    '''
    命名規則
    [モジュール名]_[エラー概要]
    '''

    # reindex.py
    REINDEX_JIRA_CHECK_FAILED = "JIRAのステータスチェックでエラーが発生しました"
    REINDEX_JIRA_BACKGROUND_REINDEX_START_FAILED = "JIRAのバックグラウンドインデックス再作成の開始に失敗しました"
    REINDEX_JIRA_BACKGROUND_REINDEX_FAILED = "JIRAのバックグラウンドインデックス再作成の開始中にエラーが発生しました"
    REINDEX_STATUS_FAILED = "JIRAのインデックス再作成のステータスが失敗しました"
    REINDEX_STATUS_CHECK_FAILED = "JIRAのインデックス再作成のステータス確認中にエラーが発生しました"
    REINDEX_TOO_LONG_TO_COMPLETE = "JIRAのインデックス再作成に時間がかかり過ぎています"
    REINDEX_WAIT_TO_COMPLETED_FAILED = "JIRAのインデックス再作成の確認中にエラーが発生しました"


    # その他
    OTHER_UNKNOWN_ERROR = "不明なエラーが発生しました"


def handle_error(error_type, exception="", message=""):
    logger.error("%s:%s" % (error_type.name, error_type.value))

    # exceptionが空でなければエラー出力
    if not exception:
        logger.exception(exception)
    
    # messageが空でなければエラー出力
    if not message:
        logger.error(message)

    # 異常コードで終了させる
    sys.exit(1)