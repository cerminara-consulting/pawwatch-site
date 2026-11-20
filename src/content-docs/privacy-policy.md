# Privacy Policy

Last updated 2026-11-20

PawWatch ("we," "our," or "the app") is published by Cerminara Consulting LLC, a Virginia-based independent consulting practice. This policy explains what information PawWatch collects, how we use it, who we share it with, and the choices you have. We designed PawWatch to collect the minimum data needed to make dog-walking safer, and nothing else.

## What we collect

### Account information

You can create an account with your email address and a password, or with Sign in with Apple. With email, we store your email address and a securely hashed version of your password; we never see or store the password itself. With Sign in with Apple, we receive an Apple account identifier and, the first time you sign in, the name and email you choose to share (which may be an Apple private relay address). We do not receive your Apple ID password.

We store your first name and use it to attribute your reports and to greet you in the app. Other signed-in walkers see your first name on reports you submit. Accounts created in earlier versions may also have a display name, which is used the same way.

When you create an account, or when our terms change, you agree to the Terms of Use and this Privacy Policy. We record when you agreed and which version, so we can show the current terms to anyone who hasn't accepted them yet.

We also store your account settings: your alert settings (on or off, and your radius), whether you use PawWatch as an owner or a walker, which shared pet you're walking, and, for our moderators, a moderator flag.

### Profile photo

If you add a profile photo, we store it and show it on your account; other signed-in walkers can see it too (for example, in their Blocked users list if they block you). Before a photo leaves your phone, the app crops it to a square, shrinks it, and re-saves it, removing all hidden information the original file carried, including GPS location, camera make and model, and the date it was taken. Photos are stored privately: only people signed in to PawWatch can view them. Signed-in users can technically list the stored photo files, which shows account and pet identifiers (random codes, not names) and upload times, but not names, emails, or locations.

### Location data

With your permission, PawWatch uses your device's location to:

- **Verify your neighborhood.** When you set up your account, you either type your address or use your current location once. We look up your neighborhood with Apple Maps, then store your home location (latitude and longitude) and your neighborhood name on your profile. Only you can see them. We do not store the address you typed.
- **Tag the reports you submit.** A report holds the category, severity, title, optional description, time, and the latitude and longitude of the pin you place on the map (it starts at your current location or your home), so other walkers can see where it happened. Once it passes moderation, every signed-in walker can see it. Nearby reports of the same hazard are grouped on the map at the location of the earliest one.
- **Show nearby hazards on the map.** We use your location to fetch hazards within walking distance and to center the map on you.
- **Track walks.** If you start a walk, we record GPS points every few seconds so you can review the route and distance afterward. Recording continues while your phone is locked until you end the walk; iOS shows the location indicator while it runs. Walks are stored in our database while your account is active and are visible only to you. They are deleted immediately when you delete the walk or your account. Until a walk's points are uploaded, they are kept on your phone so a walk survives the app closing. We also store which of your pets were on each walk, and a report you file during a walk is linked to that walk (other walkers can't see the walk).
- **Send you alerts.** If you've set a home radius, we compare new reports to your saved home location on our server and notify you when a hazard appears within your radius. This uses your saved home, not your device's live location.

You can disable location at any time in iOS Settings. PawWatch will continue to work for any features that don't require it.

### Your pets

If you add pets, we store each pet's name, breed, size, any notes you write, and an optional photo (processed and stored the same way as profile photos). Other signed-in walkers see your pet's name on reports you file while walking it. When a walker you've shared a pet with files a report, it shows that they were walking your pet for you, with your first name.

If you share a pet with another walker, we store the invite. Once accepted, the share record stays with the pet's owner until it's revoked; if the walker deletes their account, the record stays with the owner without the walker's details. If you type their email address for the invite, we keep it only while the invite is open and erase it when the invite is accepted, revoked, or expires (invites expire after 7 days). The invite code itself is stored only in a scrambled form.

### Ratings, confirmations, flags and blocks

When you rate a report, confirm it is still there, say it is gone or resolved, flag it, or block another walker, we store that action with your account. A flag's category and optional note are seen by our moderators. Your individual ratings and votes are visible only to you; other walkers see only totals (for example, "3 confirms"), which our server keeps without recording who voted in them. Blocks are visible only to you.

### On your phone

The app keeps a few things on your phone itself: your sign-in session (in the iOS Keychain), a walk in progress and any route points not yet uploaded, your theme choice, whether you've ticked the terms checkbox on this phone, and which walk milestones you've already seen. The terms tick is cleared every time the app starts, when you sign out, and when you delete your account. Signing out also clears your session; deleting your account also clears your walk data and milestones from the phone.

### Push notification tokens

If you grant notification permission, iOS gives the app a token that lets us send you push notifications through Apple. We store this token with your account and delete it when you sign out or delete your account. If someone else signs in on the same phone, the token moves to their account, so a shared phone never gets two people's alerts.

### Crash and performance data

We do not currently use a third-party crash reporter. If we add one (e.g., Sentry, Crashlytics), we'll update this policy and ask for your consent again.

## What we don't collect

- Your contacts list
- Your photo library or camera (you pick one photo at a time; the app never reads your library or uses the camera)
- Your advertising identifier (IDFA)
- Your purchase history
- Your browsing history outside the app
- Your microphone or audio

## How we use your data

We use the data above to:

- Show you hazards reported by other walkers in your area
- Attribute reports and ratings to their authors
- Send you push notifications when you have alerts enabled
- Track your walks if you choose to use the walk feature
- Let you share a pet with another walker
- Keep the map safe through moderation
- Improve the app's reliability and fix bugs

We do not use your data for advertising. We do not sell your data to third parties. We do not use your location history to build a profile of you.

## Third-party services

PawWatch relies on the following third-party services to operate. Each has its own privacy policy:

**Supabase (hosting, database, and sign-in)**
Hosts our database and server code and handles sign-in. It stores your account, profile, photos, pets, reports, ratings, walk history, invites, and notification tokens. Supabase also keeps standard request and server logs, such as IP address, time, and the address of each request, for about 7 days, then deletes them. Because the map asks for the reports in the area on screen, request logs can include the map area being loaded. Supabase's sign-in service logs each sign-up and sign-in, including your email address, in its logs, which are deleted after about 7 days. Supabase's privacy policy: [supabase.com/privacy](https://supabase.com/privacy).

**Apple (Sign in with Apple, Maps lookups, and push)**
Handles sign-in when you choose Sign in with Apple, delivers push notifications on iOS, and provides the maps. When you verify your neighborhood, the address you type (or your current location) is sent to Apple Maps to look up the area; maps you view are loaded from Apple. A push notification's text passes through Apple to reach your phone: the hazard type, its distance from your home, and, only once the report has passed review, the start of its description. If you delete an account created with Sign in with Apple, we ask Apple to revoke PawWatch's access to your Apple account. If you choose Delete without Apple instead, we don't contact Apple, and you can remove PawWatch yourself in iOS Settings (your name, Sign-In & Security, Sign in with Apple). Apple's privacy policy: [apple.com/legal/privacy](https://www.apple.com/legal/privacy/).

**OpenAI (moderation of report text)**
Checks the title and description of each new report before anyone else sees it. OpenAI receives only the report text: never your name, email, location, account, or device information. OpenAI's API data policies apply to that text. OpenAI's privacy policy: [openai.com/policies/privacy-policy](https://openai.com/policies/privacy-policy).

**Resend (account emails)**
If you sign up with email, we send account emails, such as your sign-up confirmation, through Resend, which receives your email address and the message. Resend's privacy policy: [resend.com/legal/privacy-policy](https://resend.com/legal/privacy-policy).

**People you choose to share with**
When you tap Share on a walk card or a pet invite, the image or invite message goes to whoever you send it to, through the app you pick.

Your device's location itself is handled by iOS on your phone. We do not use Google services, analytics tools, or advertising networks.

Our website, paw-watch.app, is hosted on Cloudflare, which processes visitors' IP addresses to serve its pages; the site uses no analytics or cookies.

## User-generated content and moderation

Hazard reports are user-generated content. To keep the map a safe and useful place to walk, PawWatch provides:

- **Flag any report as offensive.** Open any report and tap "Report this content." Choose a category (harassment, hate speech, off-topic, impersonation, or other) and add an optional note. Flagged reports are reviewed by a moderator within 24 hours.
- **Block another user.** Open any report and tap "Block this user" at the bottom. You will not see that user's reports on the map or in any feed. You can unblock from My Activity → Blocked users at any time.
- **Automated moderation on submission.** Before a new report is shown to anyone, its text is checked by an automated moderation service (OpenAI). The service receives only the report text, never your location, account, or device information. Reports that fail the check stay hidden until a moderator reviews them. Borderline reports stay visible but go to a moderator, and their text is left out of push alerts until they've been reviewed. If the check can't run, the report stays hidden rather than being shown unchecked.

We keep a record of each moderation decision (the outcome and the service's scores, not the report text) so decisions can be audited. These records are kept after a report or account is deleted, with the link to the account removed.

If a report you submit is removed after review, you can appeal the decision by emailing [privacy@paw-watch.app](mailto:privacy@paw-watch.app). We will respond within five business days.

We do not use your reports, your reading history, or any other user-generated content to train AI models or to build advertising profiles. PawWatch is published by a small independent consulting practice, not an ad network.

## Children's privacy

PawWatch is not intended for children under 13. We do not knowingly collect information from children under 13. If you believe a child under 13 has created an account, please contact us and we will delete it.

## Your rights

### Access, correction, and deletion

You can:

- **Update your profile** (photo, home location, alert settings) at any time: tap your photo or initial at the top left of any tab to open Account. Alert settings are in Account and on the Alerts tab.
- **Delete your reports** by opening a report you submitted and tapping "Delete report."
- **Delete a walk** from your walk history on the PawWalk tab.
- **Delete your account from inside the app** at any time: open Account (your photo or initial at the top left of any tab), scroll to the bottom, and tap Delete account. You'll be asked to type the word "delete" to confirm. Your profile, photos, pets, reports, ratings, walks, blocks, invites, alert settings, and notification tokens are removed immediately. If your account was created with Sign in with Apple, we also ask Apple to revoke PawWatch's access to your Apple account; if you choose Delete without Apple, we don't, and you can remove PawWatch in iOS Settings (your name, Sign-In & Security, Sign in with Apple). If you no longer have access to the app, you can also email [privacy@paw-watch.app](mailto:privacy@paw-watch.app) and we will delete your account within 30 days; a deletion by email can't ask Apple to revoke access, so we'll tell you how to remove PawWatch in Settings.
- **Export your data** by contacting us at [privacy@paw-watch.app](mailto:privacy@paw-watch.app). We'll send you a JSON archive of your account within 30 days.

**What stays after you delete your account.** A few records are not removed by account deletion:

- Moderation decision records, with the link to your account removed (see above).
- Totals on other people's reports that include your past ratings or votes; they hold only counts, never who voted.
- Our hosting provider's request and server logs, including its sign-in service's log of each sign-up and sign-in with your email address, until they're deleted after about 7 days.
- Report text already sent to OpenAI for moderation, under OpenAI's API retention policy.
- Reports other walkers filed while walking your pet stay on the map until they expire; your name and pet are removed from them.
- If you were a moderator, your past decisions on flagged reports stay, without your name.
- If someone you invited to walk a pet hasn't accepted yet, your invite is deleted with your account; nothing about you stays with them.

### California residents (CCPA / CPRA)

We honor the rights granted by the California Consumer Privacy Act (CCPA / CPRA) (to know what personal information we collect, to delete it, to correct it, and to limit the use of any sensitive personal information) for every user regardless of residency. We do not sell or share personal information for cross-context behavioral advertising. To exercise these rights, contact [privacy@paw-watch.app](mailto:privacy@paw-watch.app).

### European Union and United Kingdom (GDPR)

PawWatch is not currently available to residents of the European Union, the United Kingdom, or other jurisdictions outside the United States. If you are in one of those jurisdictions, please do not create an account. The Apple App Store availability setting on this app is "United States only," and the Terms of Use require U.S. residency. Should we expand availability to additional jurisdictions in the future, this section will be updated with the applicable privacy-law disclosures (including, where required, a named EU Article 27 representative and an international-data-transfer mechanism).

## Data retention

- **Active reports:** 24 hours (low severity), 72 hours (medium), or 7 days (high), then deleted, along with their ratings and confirmations. You can delete your own report sooner.
- **Walk history:** retained on your account until you delete it or delete your account.
- **Account profile, photos, and pets:** retained until you delete them or your account.
- **Invitee email addresses:** erased when the invite is accepted, revoked, or expires (7 days).
- **Push notification tokens:** deleted when you sign out or delete your account, or when Apple reports the token is no longer valid.
- **Moderation decision records:** kept for auditing, without a link to your account once you delete it.
- **Request, server, and sign-in logs:** deleted after about 7 days.

## Security

We use TLS for all data in transit. Data at rest is stored in Supabase's encrypted Postgres database. Photos are stored privately and can only be viewed by signed-in users. We follow industry practices for secrets management and access control. That said, no system is perfectly secure; if you believe your account has been compromised, contact us immediately.

## Changes to this policy

If we change this policy in a material way, we'll notify you through the app and update the "last updated" date above. If the changes are significant (e.g., a new category of data collection), we'll ask for your consent again.

## Contact

PawWatch is published by Cerminara Consulting LLC.

Email: [privacy@paw-watch.app](mailto:privacy@paw-watch.app)

**Registered agent (legal address of record)**
Cerminara Consulting LLC
c/o Northwest Registered Agent LLC
8401 Mayland Dr, Ste A
Richmond, VA 23294
United States

**Mailing address**
Cerminara Consulting LLC
Attn: PawWatch Privacy
PO Box 23
Studley, VA 23162-9997
United States
