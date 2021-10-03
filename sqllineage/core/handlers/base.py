from sqlparse.sql import Token

from sqllineage.holders import SubQueryLineageHolder


class NextTokenBaseHandler:
    """
    This is to address an extract pattern when a specified token indicates we should extract something from next token.
    """

    def __init__(self) -> None:
        self.indicator = False

    def _indicate(self, token: Token) -> bool:
        """
        Whether current token indicates a following token to be handled or not.
        """
        raise NotImplementedError

    def _handle(self, token: Token, holder: SubQueryLineageHolder, **kwargs) -> None:
        """
        Handle the indicated token, and update the lineage result accordingly
        """
        raise NotImplementedError

    def indicate(self, token: Token):
        """
        Set indicator to True only when _indicate returns True
        """
        indicator = self._indicate(token)
        if indicator:
            self.indicator = True

    def handle(self, token: Token, holder: SubQueryLineageHolder, **kwargs):
        """
        Handle and set indicator back to False
        """
        if self.indicator:
            self._handle(token, holder, **kwargs)
            self.indicator = False

    def end_of_query_cleanup(self, holder: SubQueryLineageHolder, **kwargs) -> None:
        """
        Optional hook to be called at the end of statement or subquery
        """
        pass


class CurrentTokenBaseHandler:
    """
    This is to address an extract pattern when we should extract something from current token
    """

    def handle(self, token: Token, holder: SubQueryLineageHolder) -> None:
        raise NotImplementedError