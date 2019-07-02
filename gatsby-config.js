module.exports = {
  siteMetadata: {
    title: 'Sitzplan Rat Münster',
    description: 'Der Sitzplan der Sitzungen des Rats Münster als Webseite',
    author: '@codeformuenster',
  },
  plugins: [
    `gatsby-transformer-yaml`,
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        path: `./data/`,
      },
    },
    'gatsby-plugin-react-helmet',
    {
      resolve: `gatsby-plugin-manifest`,
      options: {
        name: 'Rat Münster',
        short_name: 'Rat Münster',
        start_url: '/',
        background_color: '#005b79',
        theme_color: '#005b79',
        display: 'minimal-ui',
        icon: 'src/images/gatsby-icon.png', // This path is relative to the root of the site.
      },
    },
    // this (optional) plugin enables Progressive Web App + Offline functionality
    // To learn more, visit: https://gatsby.app/offline
    // 'gatsby-plugin-offline',
  ],
}
