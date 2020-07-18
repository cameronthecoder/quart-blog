from quart import Blueprint, render_template, redirect, abort, current_app, request, Request
blog = Blueprint("blog", __name__, template_folder="blog")

@blog.route('/')
async def index():
    query = "SELECT * FROM posts ORDER BY -created_at"
    rows = await current_app.db.fetch_all(query=query)
    return await render_template('index.html', posts=rows)


@blog.route('/post/<string:slug>/')
async def post(slug):
    query = "SELECT * FROM posts WHERE slug = :slug"
    row = await current_app.db.fetch_one(query=query, values={"slug": slug})
    if not row: abort(404)
    return await render_template("post.html", post=row)

@blog.route('/check_slug/')
async def check_slug(request: Request):
    slug = request.args.get('slug')
    query = "SELECT * FROM posts WHERE slug = :slug"
    row = await current_app.db.fetch_one(query=query, values={"slug": slug})

@blog.route('/search/')
async def search():
    q = request.args.get('query', None)
    if not q:
        return redirect('/')
    query = "SELECT * FROM posts WHERE title LIKE CONCAT('%', :query, '%') OR body LIKE CONCAT('%', :query, '%')"
    rows = await current_app.db.fetch_all(query=query, values={"query": q})
    return await render_template('index.html', posts=rows, query=q)


@blog.route('/contact/')
async def contact():
    return await render_template('contact.html')

@blog.route('/new_post/', methods=['GET', 'POST'])
async def new_post():
    if request.method == "POST":
        post = await request.get_json()
        title = post['title']
        summary = post['summary']
        body = post['body']
        image_url = 'https://static.djangoproject.com/img/logos/django-logo-negative.png'
        slug = post['slug']
        tags = post['tags']
        query = """INSERT INTO posts(title, slug, summary, body, image_url) VALUES (:title, :slug, :summary, :body, :image_url)"""
        try:
            await current_app.db.execute(query=query,
                                     values={"title": title, "slug": slug, "summary": summary, "body": body, "image_url": image_url})
            return {"message": "Success!"}
        except Exception as e:
            current_app.logger.error(e)
            return {"message": "Error"}, 500
    return await render_template('new_post2.html')


@blog.route('/edit_post/<int:id>/', methods=['GET', 'POST'])
async def edit_post(id):
    q_post = """SELECT * FROM posts WHERE id = :id"""
    row = await current_app.db.fetch_one(query=q_post, values={"id": id})
    if not row:
        return 'post not found', 404
    if request.method == "POST":
        form = await request.form
        edited_title = form.get('title')
        edited_body = form.get('body')
        edited_image_url = form.get('image_url')
        edited_slug = form.get('slug')
        # update row
        query = """UPDATE posts SET title = :title, body = :body, image_url = :image_url, slug = :slug WHERE id = :id"""
        await current_app.db.execute(query=query,
                                     values={"title": edited_title, "slug": edited_slug, "body": edited_body,
                                             "image_url": edited_image_url, "id": id})
        return redirect('/')
    return await render_template('edit_post.html', post=row)
