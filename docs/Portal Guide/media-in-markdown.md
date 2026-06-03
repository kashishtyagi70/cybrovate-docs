# Media In Markdown

Use the `/media` folder for documentation images and videos.

## Folder Layout

Place image files here:

```text
media/images/
```

Place video files here:

```text
media/videos/
```

## Add Images

Use normal Markdown image syntax:

```md
![Architecture diagram](/media/images/architecture.png)
```

Images automatically resize to stay inside the document body.

For a specific image size, add one of these classes after the image:

```md
![Small screenshot](/media/images/example.png){.media-sm}
![Medium screenshot](/media/images/example.png){.media-md}
![Large screenshot](/media/images/example.png){.media-lg}
![Centered screenshot](/media/images/example.png){.media-md .media-center}
![Full width screenshot](/media/images/example.png){.media-full}
```

You can use `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, and `.svg` files.

## Add Videos

Use the portal video shortcode:

```md
![video:Product walkthrough](/media/videos/walkthrough.mp4)
```

You can also use plain HTML if you need more control:

```html
<video controls preload="metadata" src="/media/videos/walkthrough.mp4"></video>
```

Use browser-friendly formats such as `.mp4` or `.webm`.

## Sync Markdown Files Into PostgreSQL

This portal renders documents from PostgreSQL. After editing any `.md` file, run:

```powershell
py -3.13 -m app.utils.import_docs
```

The importer scans all files in `/docs`, creates missing documents, updates changed documents, and avoids duplicate rows.
