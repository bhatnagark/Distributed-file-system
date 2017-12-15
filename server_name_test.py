import web

import dfs.nameserver

urls = (
        '127.0.0.1',
       )

app = web.application(urls, globals())


if __name__ == '__main__':
    app.run()
