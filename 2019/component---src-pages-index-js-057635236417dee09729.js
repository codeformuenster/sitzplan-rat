(window.webpackJsonp=window.webpackJsonp||[]).push([[3],{140:function(e,t,a){"use strict";a.r(t);a(73),a(75),a(32);var n=a(7),r=a.n(n),i=a(0),s=a.n(i),o=a(161),c=a(175),l=a(163),u=a.n(l),d=(a(173),s.a.memo(function(e){var t=e.label,a=e.sitz_id,n=e.partei;return s.a.createElement(s.a.Fragment,null,s.a.createElement("h4",null,t),s.a.createElement("p",null,n),s.a.createElement("div",null,s.a.createElement(u.a,{src:"https://www.stadt-muenster.de/sessionnet/sessionnetbi/im/pe"+a+".jpg"})))})),p=function(e){var t,a=e.url,n=e.partei,r=e.label;return"string"==typeof a&&(t=a.split("__kpenr=")[1]),s.a.createElement(c.a,{arrow:!0,content:s.a.createElement(d,{partei:n,label:r,sitz_id:t})},s.a.createElement("div",{className:o("sitz",n)},s.a.createElement("a",{className:"sitz-link",href:a,target:"_blank",rel:"noopener noreferrer"},r)))},m=a(149),f=a(147);a(174);a.d(t,"default",function(){return g}),a.d(t,"query",function(){return y});var g=function(e){function t(t){var a;(a=e.call(this,t)||this).onSitzClick=function(e){var t=[].concat(a.state.grid);e:for(var n=0;n<=a.state.rows;n++)for(var r=0;r<=a.state.columns;r++)if(a.state.grid[r]&&a.state.grid[r][n]&&a.state.grid[r][n].key===e){var i=[].concat(t[r]);i[n]=Object.assign({},a.state.grid[r][n],{showPopup:!a.state.grid[r][n].showPopup}),t[r]=i;break e}a.setState({grid:t})};var n=[],r=0,i=0;return t.data.allSitzeYaml.edges.forEach(function(e){var t=e.node,a=t.row,s=t.column;if(null!==a&&null!==s){if(Array.isArray(n[s])||(n[s]=[]),t.url){var o=t.url.split("__kpenr=")[1];o&&(t.img_url_id=o)}var c=s+"-"+a;n[s][a]=Object.assign({},t,{showPopup:!1,key:c}),a&&a>r&&(r=a),s&&s>i&&(i=s)}}),a.state={rows:r,columns:i,grid:n},a}r()(t,e);var a=t.prototype;return a._renderElements=function(){for(var e=[],t=0;t<=this.state.rows;t++)for(var a=0;a<=this.state.columns;a++)if(this.state.grid[a]&&this.state.grid[a][t]){var n=this.state.grid[a][t];e.push(s.a.createElement(p,n))}else e.push(s.a.createElement("div",{key:a+"-"+t}));return e},a.render=function(){return s.a.createElement(m.a,null,s.a.createElement(f.a,{title:"Sitzplan Rat",keywords:["muenster","sitzplan","rat"]}),s.a.createElement("div",{className:"sitze",style:{gridTemplateColumns:"repeat("+(this.state.columns+1)+", 1fr)",gridTemplateRows:"repeat("+(this.state.rows+1)+", 1fr)"}},this._renderElements()))},t}(i.Component),y="1221941154"},142:function(e,t,a){"use strict";a.r(t),a.d(t,"graphql",function(){return f}),a.d(t,"StaticQueryContext",function(){return p}),a.d(t,"StaticQuery",function(){return m});var n=a(0),r=a.n(n),i=a(4),s=a.n(i),o=a(141),c=a.n(o);a.d(t,"Link",function(){return c.a}),a.d(t,"withPrefix",function(){return o.withPrefix}),a.d(t,"navigate",function(){return o.navigate}),a.d(t,"push",function(){return o.push}),a.d(t,"replace",function(){return o.replace}),a.d(t,"navigateTo",function(){return o.navigateTo});var l=a(143),u=a.n(l);a.d(t,"PageRenderer",function(){return u.a});var d=a(33);a.d(t,"parsePath",function(){return d.a});var p=r.a.createContext({}),m=function(e){return r.a.createElement(p.Consumer,null,function(t){return e.data||t[e.query]&&t[e.query].data?(e.render||e.children)(e.data?e.data.data:t[e.query].data):r.a.createElement("div",null,"Loading (StaticQuery)")})};function f(){throw new Error("It appears like Gatsby is misconfigured. Gatsby related `graphql` calls are supposed to only be evaluated at compile time, and then compiled away,. Unfortunately, something went wrong and the query was left in the compiled code.\n\n.Unless your site has a complex or custom babel/Gatsby configuration this is likely a bug in Gatsby.")}m.propTypes={data:s.a.object,query:s.a.string.isRequired,render:s.a.func,children:s.a.func}},143:function(e,t,a){var n;e.exports=(n=a(145))&&n.default||n},144:function(e){e.exports={data:{site:{siteMetadata:{title:"Sitzplan Rat Münster"}}}}},145:function(e,t,a){"use strict";a.r(t);a(32);var n=a(0),r=a.n(n),i=a(4),s=a.n(i),o=a(53),c=a(2),l=function(e){var t=e.location,a=c.default.getResourcesForPathnameSync(t.pathname);return r.a.createElement(o.a,Object.assign({location:t,pageResources:a},a.json))};l.propTypes={location:s.a.shape({pathname:s.a.string.isRequired}).isRequired},t.default=l},146:function(e,t,a){},147:function(e,t,a){"use strict";var n=a(148),r=a(0),i=a.n(r),s=a(4),o=a.n(s),c=a(150),l=a.n(c),u=a(142);function d(e){var t=e.description,a=e.lang,r=e.meta,s=e.keywords,o=e.title;return i.a.createElement(u.StaticQuery,{query:p,render:function(e){var n=t||e.site.siteMetadata.description;return i.a.createElement(l.a,{htmlAttributes:{lang:a},title:o,titleTemplate:"%s | "+e.site.siteMetadata.title,meta:[{name:"description",content:n},{property:"og:title",content:o},{property:"og:description",content:n},{property:"og:type",content:"website"},{name:"twitter:card",content:"summary"},{name:"twitter:creator",content:e.site.siteMetadata.author},{name:"twitter:title",content:o},{name:"twitter:description",content:n}].concat(s.length>0?{name:"keywords",content:s.join(", ")}:[]).concat(r)})},data:n})}d.defaultProps={lang:"en",meta:[],keywords:[]},d.propTypes={description:o.a.string,lang:o.a.string,meta:o.a.array,keywords:o.a.arrayOf(o.a.string),title:o.a.string.isRequired},t.a=d;var p="1025518380"},148:function(e){e.exports={data:{site:{siteMetadata:{title:"Sitzplan Rat Münster",description:"Der Sitzplan der Sitzungen des Rats Münster als Webseite",author:"@codeformuenster"}}}}},149:function(e,t,a){"use strict";var n=a(144),r=a(0),i=a.n(r),s=a(4),o=a.n(s),c=a(142),l=function(e){var t=e.siteTitle;return i.a.createElement("div",{style:{background:"rebeccapurple",marginBottom:"1.45rem"}},i.a.createElement("div",{style:{margin:"0 auto",maxWidth:960,padding:"1.45rem 1.0875rem"}},i.a.createElement("h1",{style:{margin:0}},i.a.createElement(c.Link,{to:"/",style:{color:"white",textDecoration:"none"}},t))))};l.propTypes={siteTitle:o.a.string},l.defaultProps={siteTitle:""};var u=l,d=(a(146),function(e){var t=e.children;return i.a.createElement(c.StaticQuery,{query:"755544856",render:function(e){return i.a.createElement(i.a.Fragment,null,i.a.createElement(u,{siteTitle:e.site.siteMetadata.title}),i.a.createElement("div",{style:{margin:"0 auto",padding:0}},t))},data:n})});d.propTypes={children:o.a.node.isRequired};t.a=d},174:function(e,t,a){}}]);
//# sourceMappingURL=component---src-pages-index-js-057635236417dee09729.js.map