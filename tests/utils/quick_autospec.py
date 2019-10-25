from unittest import mock


def quick_autospec(self, list_of_targets):
    for target in list(list_of_targets):
        name = target.split('.').pop()
        patcher = mock.patch(target, autospec=True)
        mocker = patcher.start()

        self.addCleanup(patcher.stop)

        setattr(self, f'patcher_{name}', patcher)
        setattr(self, f'mock_{name}', mocker)

    return self
