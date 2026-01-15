# Website Roadmap

Future improvements to consider when time permits.

## Quick Wins (< 30 min each)

- [ ] **Add PDF CV download** - Create downloadable CV and enable the commented-out download button on cv.html
- [ ] **Static fallback for publication stats** - Add default values on publications.html like on home page (currently shows "...")
- [ ] **Improve image alt text** - More descriptive alt for profile photo (accessibility)
- [ ] **Add og:image meta tag** - Social sharing preview image

## Content Enhancements

- [ ] **Teaching section** - Add courses taught (on CV or separate page)
- [ ] **Projects/Grants section** - Current and past funded research projects
- [ ] **Media/Press mentions** - If any interviews or media coverage exists
- [ ] **Talks/Presentations** - Invited talks, keynotes

## Design Polish

- [ ] **Dark mode toggle** - Honor system preference or manual toggle
- [ ] **Print stylesheet refinement** - Optimize CV page for printing
- [ ] **Loading states** - Skeleton loaders for publications while Bibsonomy loads
- [ ] **404 page** - Custom not-found page matching site aesthetic

## Technical

- [ ] **Performance audit** - Lighthouse check, optimize images if needed
- [ ] **Sitemap.xml** - For SEO
- [ ] **robots.txt** - Basic crawl guidance
- [ ] **Analytics** - Consider privacy-friendly option (Plausible, Umami)

## Content Freshness

- [ ] **Automate citation stats** - Currently hardcoded on home; could fetch from OpenAlex on build
- [ ] **Publication sync** - Consider GitHub Action to periodically refresh publications.json from Bibsonomy
