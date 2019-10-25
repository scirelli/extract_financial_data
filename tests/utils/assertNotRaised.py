from unittest.case import _AssertRaisesContext
import traceback


class AssertNotRaisesContext(_AssertRaisesContext):
    def __exit__(self, excecution_type, excecution_value, tb):
        if excecution_type is not None:
            try:
                excecution_name = self.expected.__name__
            except AttributeError:
                excecution_name = str(self.expected)
            if self.obj_name:
                self._raiseFailure("{} raised by {}".format(excecution_name, self.obj_name))
            else:
                self._raiseFailure("{} raised".format(excecution_name))
        else:
            traceback.clear_frames(tb)
        return True


def assertNotRaised(self, expected_exception, *args, **kwargs):
    context = AssertNotRaisesContext(expected_exception, self)
    try:
        return context.handle('assertNotRaised', args, kwargs)
    finally:
        context = None
