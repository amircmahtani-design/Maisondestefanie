/* ============================================================
   La Maison de Stefanie — configuration
   This is the ONLY file you need to edit to connect the Studio.
   Everything else is managed from the Studio in the browser.
   ============================================================ */

window.LMS_CONFIG = {

  /* ---- 1. Firebase (optional, but recommended) -------------
     With Firebase filled in, Stefanie edits the site from the
     Studio and it goes live instantly — no re-uploading files.

     Get these from console.firebase.google.com
     → Project settings → Your apps → Web app → SDK config.
     Leave the placeholders as they are to run in Offline mode
     (the Studio then saves to the browser and exports a zip).
  ---------------------------------------------------------- */
  firebase: {
    apiKey:            "PASTE_API_KEY",
    authDomain:        "PASTE_PROJECT.firebaseapp.com",
    projectId:         "PASTE_PROJECT_ID",
    storageBucket:     "PASTE_PROJECT.appspot.com",
    messagingSenderId: "PASTE_SENDER_ID",
    appId:             "PASTE_APP_ID"
  },

  /* Only these email addresses may sign in to the Studio.
     They must also be listed in the Firestore security rules
     (see README, step 4).                                    */
  adminEmails: [
    "stefanie@lamaisondestefanie.com"
  ],

  /* ---- 2. Site basics -------------------------------------- */
  siteUrl: "https://lamaisondestefanie.com",

  /* Where AI writing help is served from. Leave as is if you
     deploy on Netlify. The Studio hides AI buttons when this
     is not reachable, so the site still works without it.    */
  aiEndpoint: "/.netlify/functions/ai",

  /* ---- 3. House look ---------------------------------------
     Default treatment applied to every photo Stefanie uploads
     so the whole catalogue looks like one collection. She can
     tune these live in Studio → House look, and the values are
     saved with the content.                                  */
  houseLook: {
    canvas:       1400,   // output size in pixels (square)
    cutout:       true,   // lift the product off its background
    tolerance:    34,     // how aggressively to remove the background
    feather:      1.6,    // edge softness in pixels
    subjectScale: 0.74,   // how much of the frame the product fills
    baseline:     0.90,   // where the product stands in the frame
    backdropTop:    "#efe8e0",
    backdropBottom: "#d8ccc3",
    shadow:       0.34,   // contact shadow strength
    warmth:       0.16,   // amber shift
    contrast:     0.14,
    saturation:  -0.06,
    grain:        0.05,
    vignette:     0.22,
    maxKB:        360     // compress until under this size
  }
};
