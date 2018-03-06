from organization import Organization
from pipedriver import PipeDriver

if __name__ == '__main__':
    pipe_driver = PipeDriver('a7098337502aacd4a642156eb8131e48eb8b7d31')
    pipe_driver.get_organizations()