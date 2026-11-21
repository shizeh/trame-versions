// Ancienne adresse trame.shizeh.workers.dev : tout part vers trame.shizeh.com
// (redirection permanente, pour que Google ne voie qu'un seul site).
// Exception : les images du statut Discord, encore lues ici par Trame 2.6.x.
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname.startsWith("/discord/")) return env.ASSETS.fetch(request);
    return Response.redirect(`https://trame.shizeh.com${url.pathname}${url.search}`, 301);
  },
};
