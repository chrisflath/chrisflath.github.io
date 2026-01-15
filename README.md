# Academic Website - Prof. Dr. Christoph M. Flath

A clean, professional academic website built for GitHub Pages deployment.

## Quick Start

1. **Fork or clone this repository**
2. **Enable GitHub Pages** in repository settings (Settings → Pages → Source: main branch)
3. **Customize your content** by editing the HTML files
4. Your site will be live at `https://yourusername.github.io/repository-name/`

## Structure

```
academic-website/
├── index.html          # Homepage with bio, research interests, metrics
├── publications.html   # Publications with Bibsonomy integration
├── research.html       # Research areas and current projects
├── cv.html             # Curriculum Vitae
├── css/
│   └── style.css       # Main stylesheet (easily customizable)
├── js/
│   └── main.js         # JavaScript (navigation, Bibsonomy API)
├── images/             # Place your profile photo here
└── README.md
```

## Customization

### Personal Information
Edit each HTML file to update:
- Name and title
- Affiliation
- Research interests
- Publications (static list as backup)
- CV details
- Contact information

### Profile Photo
Replace the placeholder in `index.html`:
1. Add your photo to the `images/` folder (e.g., `images/profile.jpg`)
2. Update the `<img>` tag in `index.html`:
   ```html
   <img src="images/profile.jpg" alt="Your Name" class="profile-image">
   ```

### Bibsonomy Integration
The publications page can dynamically load from Bibsonomy. Configure in `js/main.js`:
```javascript
const BIBSONOMY_CONFIG = {
    username: 'your-username',
    apiKey: 'your-api-key',
    baseUrl: 'https://www.bibsonomy.org/api',
    resourceType: 'bibtex'
};
```

**Note:** The API key is visible in client-side code. Bibsonomy's API has rate limiting, which provides some protection. For production, consider a server-side proxy.

### Colors & Styling
Edit CSS variables in `css/style.css`:
```css
:root {
    --primary-color: #1a365d;      /* Deep blue */
    --secondary-color: #2c5282;    /* Medium blue */
    --accent-color: #3182ce;       /* Bright blue */
    /* ... more variables ... */
}
```

## Deployment Options

### Option 1: GitHub Pages (Recommended)
1. Create a new repository on GitHub
2. Push this code to the repository
3. Go to Settings → Pages
4. Select "main" branch as source
5. Your site will be at `https://username.github.io/repo-name/`

### Option 2: Custom Domain
1. Add a CNAME file with your domain: `www.yourname.com`
2. Configure DNS with your domain provider
3. Enable HTTPS in GitHub Pages settings

### Option 3: University Hosting
Upload all files to your university web space via FTP/SFTP.

## Extending the Site

The codebase is designed for easy extension:

- **Add new pages**: Copy an existing HTML file and modify
- **Add blog/news**: Create a `news.html` page with a similar structure
- **Add teaching page**: Create `teaching.html` for course information
- **Add analytics**: Include Google Analytics or Plausible script

## Browser Support

- Chrome, Firefox, Safari, Edge (latest versions)
- Mobile-responsive design
- Print-friendly styling

## License

Feel free to use and modify this template for your academic website.

---

Created for Prof. Dr. Christoph M. Flath, University of Würzburg
