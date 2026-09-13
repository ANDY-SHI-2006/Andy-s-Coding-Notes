[[Microsoft Outlook-中文版|中文版 →]]

# 1 Introduction to Outlook 2016
## 1.1 Interface Overview and Customization?

### 1.1.1 Interface Components

![[ch1-main-window.png|697]]

| Area | Location | Function |
|------|------|------|
| Ribbon（功能区） | Top of the window | Organizes all commands under tabs such as Home（开始） / Send/Receive（发送/接收） / Folder（文件夹） / View（视图） |
| Quick Access Toolbar（快速访问工具栏） | Next to the title bar | Holds the most-used commands (e.g. Send/Receive（发送/接收）, Undo（撤销）); customizable |
| Navigation Pane（导航窗格） | Left side | Switch between Mail（邮件）, Calendar（日历）, People（人员）, Tasks（任务）, and lists the mailbox folders |
| Message List（邮件列表） | Middle | Shows the messages in the current folder |
| Reading Pane（阅读窗格） | Right side or bottom | Preview content without opening the message |
| To-Do Bar（微软待办栏） | Far right | Summarizes Calendar, People, and Tasks (including flagged follow-up emails) |

![[ch1-to-do-bar-dropdown.png|459]]

On the "View（视图）" tab, in the "Layout（布局）" group, click "To-Do Bar（微软待办栏）" to check "Calendar（日历(C)）", "People（人员(P)）", and "Tasks（任务(T)）"; choose "Off（关闭(O)）" to hide the To-Do Bar.

### 1.1.2 Common Customizations

1. **Collapse the ribbon**: double-click any tab name, or press `Ctrl` + `F1`, to keep only the tab titles and free up space for the message list; press again to restore.
2. **Customize the Quick Access Toolbar（快速访问工具栏）**: click the drop-down arrow on the right of the toolbar to check common commands, or right-click any ribbon button and choose "Add to Quick Access Toolbar（添加到快速访问工具栏）".
3. **Adjust the Navigation Pane（导航窗格）**: click "…" at the bottom of the navigation pane to adjust the displayed modules and their order; drag the pane's edge to change its width.

## 1.2 How to Check Mailbox Size and Usage?

1. Click **File（文件）** → **Info（信息）**.

![[ch1-file-tab.png]]

2. In the "Mailbox Settings（邮箱设置）" area (next to the "Tools（工具）" button), you can see the mailbox usage, e.g. "46.6 GB free of 49.5 GB（49.5 GB 中 46.6 GB 可用）".

![[ch1-mailbox-usage.png]]

**Note**: Exchange corporate mailboxes have quota limits. You'll get a warning when the mailbox is nearly full, and once over the limit you can't send or receive normally — clean up or archive promptly (see [[#5.5 How to Archive Emails?]]).

## 1.3 How to Find the Outlook Web Access Link?

1. Click **File（文件）** → **Info（信息）**.

![[ch1-file-tab.png]]

2. Under "Access this account on the web.（在网上访问此帐户。）" in the "Account Settings（帐户设置）" area, the **OWA (Outlook Web App) web access link** for this mailbox is displayed (e.g. `https://outlook.office365.com/owa/...`).

![[ch1-owa-url.png]]

**Use**: when you're away from your own computer (business trips, public computers), open this link in a browser and log in with your account and password to send and receive emails in web Outlook — no client configuration needed.

## 1.4 How to Add an Account Photo?

1. Click **File（文件）** → **Info（信息）**.

![[ch1-file-tab.png]]

2. Click **Change（更改）** at the account avatar and upload a local picture.

![[ch1-account-photo-placeholder.png]]

**Note**: the account photo syncs to the server via Exchange, and colleagues in your organization will see it when they receive your emails or browse the address book — use a formal personal photo.

# 2 How to Set Up and Use Email Signatures?

## 2.1 What Is an Email Signature and How to Customize It?

### 2.1.1 What Is an Email Signature

An email signature is a **block of information automatically appended to the end of every email**, usually containing your name, title, company, contact details, etc. Set it once and Outlook includes it automatically when you write emails — no need to type it every time.

### 2.1.2 How to Create One

1. Open a **new email** window.
2. Click the **Insert（插入）** tab on the ribbon → **Signature（签名）** → **Signatures（签名）** (opens the "Signatures and Stationery（签名和信纸）" window; the "Message（邮件）" tab has the same "Signature（签名）" entry).

![[ch2-signature-button.png|697]]

3. Click **New（新建(N)）** and enter a signature name (e.g. "Work Signature（工作签名）").
4. In the "Edit signature（编辑签名(I)）" area below, enter the signature content; you can set the font, size, and color, and insert a picture, company logo, or electronic business card ("Business Card（名片(B)）"); click "Save（保存(S)）" when done.

![[ch2-signature-editor.png]]

5. Click "OK（确定）" to save.

### 2.1.3 Notes

- Recommended signature content: **name, title, company, phone, email**, so the other party can reach you easily.
- Don't insert oversized pictures — every email gets bigger, and some mailboxes treat the picture as an attachment.
- You can create **multiple signatures** (e.g. Chinese, English, and a short version) and choose as needed when sending (see 2.3).

## 2.2 How to Use Different Signatures for New Emails vs. Replies and Forwards?

1. Open the "Signatures and Stationery（签名和信纸）" window (new email → "Message（邮件）" tab → "Signature（签名）" → "Signatures（签名）").
2. In the **"Choose default signature（选择默认签名）" area at the top right** of the window:
   - **"New messages（新邮件(M)）"**: choose the full signature (with logo and complete contact details).
   - **"Replies/forwards（答复/转发(F)）"**: choose the short signature (just name and phone is enough).

![[ch2-default-signature.png]]

3. Click "OK（确定）".

**Note**: using a short signature for replies and forwards prevents signatures from piling up as emails go back and forth, keeping the thread cleaner.

## 2.3 How to Choose the Signature You Need When Sending?

**Click Signature to choose manually**: to temporarily switch signatures while writing, click the "Signature（签名）" button on the ribbon of the new email window; the drop-down lists all created signatures (e.g. R&F, SHIHAOYU) — click the one you need to insert it; click "Signatures（签名(S)...）" to open the "Signatures and Stationery（签名和信纸）" window for management.

![[ch2-signature-dropdown.png]]

# 3 How to Send Emails?

## 3.1 How to Quickly Enter Recipient Addresses?

### 3.1.1 Manual Entry + Check Name（检查姓名）

![[ch3-check-name-dialog.png]]

### 3.1.2 Choose from the Address Book

![[ch3-select-names-dialog.png]]

![[ch3-address-book-button.png]]

## 3.2 Difference Between To（收件人） / CC（抄送） / BCC（密件抄送）

![[ch3-bcc-field-visible.png]]

By default, the new email window doesn't show the "BCC（密件抄送）" field. Click the **Options（选项）** tab on the ribbon → the **Bcc（密件抄送）** button to display the field (as shown above).

| Field | Full Name | Chinese | Visible to Each Other? | Typical Use Cases |
|------|------|------|-------------|-------------|
| To | - | 收件人 | Visible to everyone | The main audience, expected to handle or reply directly |
| CC | Carbon Copy | 抄送 | Visible to everyone | Needs to know about it, but not the main handler |
| BCC | Blind Carbon Copy | 密件抄送 | Invisible to To/CC; BCC recipients can't see each other | Discreetly notify someone, or protect privacy in mass emails |

### 3.2.1 Core Differences

**To（收件人）**: the main audience of the email, who must handle it.
**CC（抄送）**: secondary audience — only needs to be informed, not required to act.
**BCC（密件抄送）**: secretly sent to someone; the other recipients have no idea they received the email.

### 3.2.2 Who Can See Whom?

From a given recipient's perspective:

| If you are... | Can you see To? | Can you see CC? | Can you see BCC? |
|------------|---------------|---------------|------------------|
| Someone in To | ✅ Yes | ✅ Yes | ❌ No |
| Someone in CC | ✅ Yes | ✅ Yes | ❌ No |
| Someone in BCC | ✅ Yes | ✅ Yes | ❌ No (can't see the other BCCs) |
| The sender | ✅ Yes | ✅ Yes | ✅ Yes |

In other words:
- **People in To and CC can see each other**.
- **People in BCC can see To and CC**, but To and CC can't see BCC.
- **People in BCC can't see each other either**.

### 3.2.3 When to Use BCC?

1. **Protect privacy in mass emails**
   - When notifying a whole class or the whole company, put everyone in BCC.
   - Then each person sees only their own address, not anyone else's.

2. **Discreetly notify a third party**
   - Let a manager, HR, or auditors know about something without letting the main recipients know.

3. **Protect sensitive relationships**
   - For example, BCC your own manager on a customer email so the customer doesn't know the manager is watching.

### 3.2.4 Notes

- **If a BCC recipient clicks "Reply All（全部答复）"**, their reply goes only to the sender and the To/CC recipients, not to the other BCC recipients.
- **BCC recipients cannot tell from the email itself who else was BCC'd**.
- If you mistakenly put someone who should be confidential in To or CC, everyone will see it, and that visibility can't be revoked.

## 3.3 How to Flag Important Emails?

### 3.3.1 Importance

![[ch3-importance-buttons.png]]

Outlook provides two importance levels to tell recipients how urgent an email is:

| Level | Icon | Meaning | Recommendation |
|------|------|------|----------|
| High importance（高重要性） | Red exclamation mark | Urgent email, needs priority handling | Use only when truly urgent; overuse makes people numb to it |
| Low importance（低重要性） | Blue down arrow | Not urgent, can be handled later | Good for mass announcements, FYI-type emails |
| Default | No icon | Normal email | Use the default in most cases |

**Note**: the importance flag is visible to recipients, but it's only a visual cue — it doesn't force them to prioritize.

### 3.3.2 Follow Up

![[ch3-follow-up-dropdown.png]]

The follow-up flag mainly **reminds the sender themselves** to follow up on an email, but recipients also see a small flag icon.

| Use Case | Description |
|---------|------|
| Set when sending | After the email is sent, it appears in the sender's own "To-Do/Follow Up（待办/跟进）" list, with a reminder at the due time |
| Set when receiving | Flag emails you've received to remind yourself to handle them later |
| Recipient's view | They can see a flag on the email, but no pop-up reminder appears on their computer |

**Note**: the follow-up flag is **not a forced reminder** — it's more like a memo plus a visual cue.

### 3.3.3 Retention Policy

![[ch3-retention-policy-dropdown.png]]

The retention policy（分配策略） assigns **retention, archiving, or deletion rules** to emails, mainly used in corporate or school mailboxes (Exchange/Office 365).

| Point | Description |
|------|------|
| What it affects | Only the sender's own mailbox copies (e.g. "Sent Items（已发送邮件）") |
| Does it affect recipients | No — the recipient's copy is governed by their own mailbox policies |
| Common policies | Delete after 1 week, 1 month (30 days), 6 months, 1 year, 5 years, or never delete |
| Personal users | Regular personal mailboxes usually don't have this feature, or the button is greyed out |

**Note**: if the mailbox administrator hasn't configured policies, this button may be unusable.

## 3.4 How to Schedule Delayed Delivery?

### 3.4.1 Why Schedule Sending?

Delayed delivery isn't about letting the email "float for a while" — it's about choosing a better delivery time. Common reasons:

- **Increase the chance of being seen**: delivered after the recipient starts work, when their inbox is emptiest, the email sits higher up and is more likely to be seen.
- **Avoid disturbing rest time**: if you finish an email late at night or on the weekend, schedule it for working hours — it looks more professional.
- **Cross-time-zone communication**: schedule delivery for a workday morning in the recipient's time zone instead of staying up late to send it.
- **Plan ahead**: holiday greetings, weekly reports, meeting reminders, etc. can be written in advance and scheduled for the right time.

**Note**: delayed delivery depends on Outlook running. If the computer is off or Outlook isn't open at the scheduled time, the email may not send until the next time Outlook opens.

### 3.4.2 How to Set Up Delayed Delivery?

1. After writing the email, click the **Options（选项）** tab on the ribbon.
2. Find the **Delay Delivery（延迟传递）** button.
3. In the pop-up window, check **Do not deliver before（传递不早于）** and set the specific date and time.
4. Click **Close（关闭）**.
5. Click "Send（发送）". The email first goes to the **Outbox（发件箱）** and is sent automatically at the set time.

![[ch3-delay-delivery-dialog.png]]

### 3.4.3 Cancel or Modify

- Before sending: if you haven't clicked "Send（发送）" yet, just change the time.
- After sending but before the scheduled time: find the email in the "Outbox（发件箱）", double-click to open it, then delete it or reset the time.

## 3.5 How to Send an Email as an Attachment?

### 3.5.1 Why Send as an Attachment?

Forwarding an email as an attachment, instead of clicking "Forward（转发）" directly, has these benefits:

- **Preserves complete original info**: including the original sender, recipients, CC, timestamps, message headers, etc.
- **Avoids formatting corruption**: direct forwarding sometimes changes the original layout; the attachment form is more complete.
- **Forward multiple emails at once**: you can package several emails as attachments in one go.
- **As evidence or archive**: when you need to submit email records, the attachment form is more formal.

### 3.5.2 Method 1: Copy + Paste

1. In the message list, right-click the email you want to attach.
2. Choose **Copy（复制）** (or press `Ctrl` + `C`).

![[ch3-message-copy-context-menu.png|415]]

3. Open a new email and right-click in the body area.
4. Choose **Paste（粘贴）** (or press `Ctrl` + `V`).
5. The original email appears in the new email as a `.msg` attachment.

![[ch3-pasted-msg-attachment.png]]

### 3.5.3 Method 2: Insert via "Attach Item"

1. In a new email, click the **Message（邮件）** tab on the ribbon.
2. Click the drop-down arrow next to the **Attach File（附加文件）** button.
3. Choose **Attach Item（附加项目）** → **Outlook Item（Outlook 项目）**.

![[ch3-attach-outlook-item-menu.png]]

4. In the dialog that pops up, select the email to insert.
5. You can insert it as an **Attachment（附件）** (default) or as **Text Only（纯文本）**.

![[ch3-insert-outlook-item-dialog.png]]

6. Click **OK（确定）** and the email is added as an attachment.

**Note**: if the attached email itself has attachments, they are preserved inside the original email.

### 3.5.4 Method 3: Drag and Drop

1. In the message list, hold the left mouse button on the email you want to attach.
2. Drag it directly into the body area of the new email.
3. Release the mouse — the original email appears in the new email as a `.msg` attachment.

**Note**: if you select multiple emails and drag them together, you can attach several emails at once.

## 3.6 How to Remedy a Mis-sent Email?

### 3.6.1 When Can You Recall?

Outlook's "Recall This Message（撤回邮件）" feature is **not all-powerful** — its success rate depends on these conditions:

| Condition | Can You Recall? |
|------|---------|
| Sender and recipient are in the same Exchange/Office 365 organization | ✅ Usually yes |
| Recipient uses the Outlook client (not web/mobile) | ✅ Higher success rate |
| Recipient hasn't read the email yet | ✅ More likely to succeed |
| Recipient uses an external mailbox (e.g. Gmail, QQ, 163) | ❌ Almost impossible |
| Recipient has already read or forwarded it | ❌ Cannot recall |
| The email has left the internal server | ❌ Cannot recall |

**Summary**: recall works best between internal Exchange mailboxes in a company/school; it's basically ineffective for external mailboxes.

### 3.6.2 How to Recall an Email?

1. Open Outlook's **Sent Items（已发送邮件）** folder.
2. Double-click to open the email you want to recall.
3. Click the **Message（邮件）** tab on the ribbon.
4. Click **Actions（操作）** → **Recall This Message（撤回该邮件）**.
5. In the dialog that pops up, choose:
   - **Delete unread copies of this message（删除该邮件的未读副本）**: recall directly, leaving no trace.
   - **Delete unread copies and replace with a new message（删除未读副本并用新邮件替换）**: after recalling, a new email editing window opens automatically.
   - You can check **Tell me if recall succeeds or fails for each recipient（告诉我对每个收件人的撤回操作是成功还是失败）** (checked by default); the recall result is sent to you by email.
6. Click **OK（确定）**.

![[ch3-recall-message-menu.png]]

![[ch3-recall-message-dialog.png|395]]

### 3.6.3 What If Recall Fails?

If recall fails or isn't possible, remedy it with:

1. **Send a clarification email**
   - Use a subject like "Addendum / Correction / Regarding the Previous Email".
   - Clearly state in the body what was wrong in the previous email and what the correct content is.

2. **Resend the correct version**
   - If the previous email's attachment/content was wrong, resend the complete correct version, marking the subject with "this version prevails".

3. **Contact the recipient proactively**
   - For important emails, call or send an instant message explaining the situation and asking them to ignore the previous email.

### 3.6.4 Notes

- **Recall is not guaranteed**: even if the system reports "recall succeeded", the recipient may still have seen the email before the recall.
- **Read/unread is judged by the message state in the recipient's Outlook**: if the recipient has read the email but manually right-clicks to mark it as "unread（未读）" again, then from the perspective of Outlook's recall mechanism it is still "unread" and could theoretically still be recalled. But this depends on the recipient's specific actions and can't be relied on.
- **Don't overuse recall**: frequent recalls look unprofessional.
- **Check before sending**: build the habit of checking recipients, subject, attachments, and body before sending to reduce mistakes.

# 4 How to Reply to Emails?

## 4.1 How to Reply to an Email?

### 4.1.1 Difference Between Reply and Reply All

| Action | Replies To | When to Use |
|------|---------|---------|
| Reply（答复） | Only the sender | When you only want to communicate with the sender |
| Reply All（全部答复） | The sender + everyone in To and CC | When everyone in the thread should see your reply |

![[ch4-reply-vs-reply-all.png]]

### 4.1.2 Example

Suppose Manager Zhang（张经理） sends an email:
- **From**: Manager Zhang（张经理）
- **To**: You, Xiao Li（小李）
- **CC**: Director Wang（王总监）

You click **Reply（答复）** → in the email you send:
- **To**: Manager Zhang（张经理）
- **CC**: (empty)

You click **Reply All（全部答复）** → in the email you send:
- **To**: Manager Zhang（张经理）, Xiao Li（小李） (the original sender + the others in the original To)
- **CC**: Director Wang（王总监） (the people in the original CC)

### 4.1.3 Notes

- "Reply All（全部答复）" doesn't go to people in BCC（密件抄送） — because you can't see them at all.
- With "Reply All", you yourself won't appear in To/CC — Outlook removes you automatically.
- In group emails, think before clicking "Reply（答复）": does everyone need to see it? Avoid misusing "Reply All" and disturbing people. For example, clicking "Reply All" in a 50-person mass email sends your reply to everyone.

## 4.2 How to Forward an Email?

### 4.2.1 Forwarding

Forward the received email as-is to others; the recipient can see the original content and attachments.

![[ch4-forward-as-attachment-menu.png|577]]

| Point | Description |
|------|------|
| Original content | Automatically included in the new email body (with original sender, time, etc.) |
| Original attachments | Included by default |
| What you can change | You can add your own notes, trim content, or add/remove attachments before sending |

**When to use**:
- Pass received notices or materials to the people who need them.
- Forward a problem email to someone who can handle it, with your own explanation attached.

**Note**: before forwarding, check the original content to confirm there's nothing unsuitable for the new recipient (e.g. internal discussions, private content).

### 4.2.2 Forward as Attachment

Send the whole email as a `.msg` attachment instead of bringing the content into the body.

| Comparison | Normal Forward | Forward as Attachment |
|--------|---------|-------------|
| How the original appears | Content shown in the body | As a `.msg` attachment |
| Completeness of original info | May be altered or formatting corrupted | Fully preserved (sender, time, headers, etc.) |
| Forwarding multiple emails at once | Inconvenient | Can attach multiple emails at once |
| How the recipient opens it | Read directly | Double-click the attachment (requires Outlook) |

**How to do it** (see [[#3.5 How to Send an Email as an Attachment?]]):
1. Copy and paste: right-click to copy in the message list, paste into the new email body.
2. Attach item: in a new email, "Attach File（附加文件）" → "Attach Item（附加项目）".
3. Drag and drop: drag the email directly into the new email body.
4. Menu command: while reading the email, click "…" next to "Forward（转发）" → "Forward as Attachment（作为附件转发(F)）" (see the screenshot above).

**When to use**:
- When you need to submit email records as evidence or archive.
- When the original email information must be fully preserved.

## 4.3 How to Use Inline Comments Automatically in Email Threads?

### 4.3.1 What Is the Comments Feature?

In back-and-forth email threads, if you want to insert your own words **inside the quoted body of the original email** (rather than writing at the very top), you can enable the comments feature: each paragraph you insert is automatically prefixed with `[your name]`, so others can tell at a glance what you said versus the original text.

### 4.3.2 How to Enable It?

1. Click "File（文件）" → "Options（选项）" → "Mail（邮件）".
2. Find the "Replies and forwards（答复和转发）" section.

![[ch4-replies-and-forwards-options.png|433]]

3. Check **Mark my comments with（在批注前面加上(A)）** and enter your name in the text box (e.g. Zhang San（张三 San Zhang）).

![[ch4-mark-comments-with-name.png|449]]

4. Click "OK（确定）".

### 4.3.3 Effect

- **Works for both replies and forwards**: whether you click "Reply（答复）", "Reply All（全部答复）", or "Forward（转发）", as long as you type inside the quoted body of the original email, `[your name]` is automatically prefixed.
- In multi-person discussions, each person's comments carry their own name, making it clear at a glance who said what in the thread.

![[ch4-inline-comments-example.png|623]]

**Example:**

A paragraph in the original email:

> The meeting is set for Wednesday afternoon. Please confirm.

After you type your comment below that line, it shows as:

> The meeting is set for Wednesday afternoon. Please confirm.
> [Zhang San] I have a class on Wednesday afternoon — can we move it to Thursday?

**Note**: it's recommended to write your name in both Chinese and English (e.g. `张三 San Zhang`) for communicating with overseas colleagues.

## 4.4 How to Set Up Automatic Replies When on Leave?

### 4.4.1 How to Set It Up?

1. Click **File（文件）** → the "Account Information（帐户信息）" page.

![[ch4-file-tab.png]]

2. Click **Automatic Replies (Out of Office)（自动答复(外出)）**.

![[ch4-account-info-automatic-replies.png|401]]

3. Select **Send automatic replies（发送自动答复(S)）**.
4. (Optional) Check **Only send during this time range（只在以下时间范围内答复(O)）** and set the start and end times — it turns on and off automatically, no manual action needed.
5. Write your automatic reply content in the text box.

![[ch4-automatic-replies-dialog.png|445]]

6. Click "OK（确定）".

### 4.4.2 Separate Settings for Inside and Outside the Organization

Automatic replies have two tabs where you can write different content:

| Tab | Replies To | Content Suggestions |
|--------|------|---------|
| Inside My Organization（在我的组织内） | Colleagues in your unit (same Exchange organization) | Can be more detailed, e.g. leave dates, emergency contact |
| Outside My Organization（在我的组织外） | People with external mailboxes | Keep it brief to avoid leaking too much internal info |

### 4.4.3 Notes

- **Each sender gets only one automatic reply**: someone who emails you repeatedly only receives the auto-reply the first time, not every time.
- Automatic replies are executed by the Exchange server, **so they work even if your computer is off and Outlook isn't open** (unlike delayed delivery).
- Remember to check and turn off automatic replies when you're back from leave (if you didn't set a time range).
- Suggested content: start/end dates of your leave, and an emergency contact with their details.
# 5 Efficient Mailbox Management

## 5.1 How to Display Emails as Conversations?

### 5.1.1 What Is Conversation View?

Emails on the same topic are **collapsed into one group** instead of scattered individually by time. Expand a conversation to see the whole thread — great for tracking multi-person discussions.

![[ch5-conversation-view-collapsed.png]]

![[ch5-conversation-view-expanded.png]]

### 5.1.2 How to Enable It?

1. Click the **View（视图）** tab on the ribbon.

![[ch5-view-tab.png]]

2. In the "Messages（邮件）" group, check **Show as Conversations（显示为对话）**.

![[ch5-show-as-conversations-checkbox.png]]

3. In the dialog that pops up, choose the scope:
   - **This folder（此文件夹(T)）**: applies only to the current folder (e.g. Inbox).
   - **All mailboxes（所有邮箱(A)）**: applies to all folders.

![[ch5-conversations-scope-dialog.png]]

4. After enabling, you can fine-tune the display via **Conversation Settings（对话设置）** below (e.g. whether to show messages from other folders, whether to always expand).

### 5.1.3 Notes

- A "conversation（对话）" is grouped by **email subject and the reference relations in message headers**; if the subject changes, it may be split into different conversations.
- Be careful when deleting a whole conversation in conversation view — it deletes the entire thread together.

## 5.2 How to Flag Emails for Follow-up and Set Reminders?

### 5.2.1 What Is a Follow-up Flag?

Put a **small flag marker** on emails that need follow-up to remind yourself to handle them later. Flagged emails enter the "To-Do（待办事项）" list, and you can set a pop-up reminder at a specific time.

### 5.2.2 How to Set It Up?

1. In the message list, **right-click** the email to flag (or click the flag icon on the right of the email — the default is "Today（今天）").

![[ch5-follow-up-flag-icon.png|309]]

2. Choose a follow-up time from the menu:
   - **Today（今天(T)） / Tomorrow（明天(O)） / This Week（本周(W)） / Next Week（下周(N)） / No Date（无日期(A)）**: quick settings.
   - **Custom（自定义(C)...）**: freely set the flag name, start date, and due date.

![[ch5-follow-up-flag-menu.png|379]]

3. For a timed reminder, click **Add Reminder（添加提醒(R)...）**; in the "Custom（自定义）" window that pops up:
   - In the **Flag to（标志(F)）** drop-down, choose a flag name (e.g. "Follow up（需后续工作）").
   - Set **Start date（开始日期(S)） / Due date（截止日期(D)）**.
   - Check **Reminder（提醒(R)）** and choose the specific date and time (a pop-up will remind you at that time).

![[ch5-follow-up-add-reminder-menu.png|377]]

![[ch5-custom-flag-reminder-dialog.png|390]]

4. Click "OK（确定）".

### 5.2.3 Managing Flagged Items

| Action | Description |
|------|------|
| Mark Complete（标记完成(M)） | After finishing the task, click "Mark Complete"; the flag becomes a check mark and the email no longer appears in the to-do list |
| Clear Flag（清除标记(E)） | Click "Clear Flag" to remove the flag directly |
| Set Quick Click（设置快速单击(Q)...） | Customize the default behavior when you click the flag icon (default is "Today（今天）") |

### 5.2.4 Notes

- For emails with reminders, **Outlook must be open** at the set time for the pop-up to appear.
- In the reminder pop-up, you can choose "Dismiss（消除）" (no more reminders) or "Snooze（暂缓）" (remind again later).
- All flagged emails can be viewed together in "To-Do（待办事项）", or managed centrally with a search folder (see 5.3).

## 5.3 How to Create a Follow-up Search Folder?

### 5.3.1 What Is a Search Folder?

A search folder is a **virtual folder**: it aggregates all emails matching set conditions for display, but the emails themselves stay in their original folders — they aren't moved or copied.

![[ch5-search-folders-nav-pane.png|201]]

### 5.3.2 How to Create One

![[ch5-new-search-folder-menu.png|224]]

![[ch5-new-search-folder-dialog.png|276]]

1. In the left navigation pane, right-click **Search Folders（搜索文件夹）** → **New Search Folder（新建搜索文件夹(S)...）** (or click the "Folder（文件夹）" tab on the ribbon → "New Search Folder（新建搜索文件夹）").
2. In the "Select a Search Folder（选择搜索文件夹(S)）" list, choose **Mail flagged for follow up（标有后续标志的邮件）** (under the "Reading Mail（读取邮件）" category).
3. Click "OK（确定）". It then appears under **Search Folders（搜索文件夹）** in the left navigation pane, where all emails with Follow-up flags are shown together.

### 5.3.3 Notes

- Deleting a search folder **does not delete the emails themselves** — it only removes this aggregated view.
- Once an email is unflagged or marked complete, it automatically disappears from the search folder.
- Combined with the Follow-up feature in 5.2, it acts as an auto-updating "to-follow-up email list".

## 5.4 How to Save an Email?

### 5.4.1 Save As a File

![[ch5-file-tab-on-email.png]]

![[ch5-save-as-menu.png|131]]

![[ch5-save-as-formats.png|700]]

1. Double-click to open the email you want to save.
2. Click **File（文件）** → **Save As（另存为）** (shortcut: `F12`).
3. Choose the save location and format:
   - **`.msg`**: Outlook message format; double-click to reopen, keeps full formatting and attachments ("Save as type（保存类型(T)）" defaults to "Outlook Message Format - Unicode(*.msg)（Outlook 邮件格式 - Unicode(*.msg)）").
   - **`.txt` / `.html`**: plain text or web format, more universal.
   - The "Save as type（保存类型(T)）" drop-down also offers Outlook Template (`.oft`), MHT files (`.mht`), etc.

### 5.4.2 Drag to Save

1. In the message list, hold the left mouse button on the email.
2. Drag it directly onto the **desktop or any folder** and release — it saves as a `.msg` file.

### 5.4.3 Notes

- `.msg` files **require Outlook to be installed to open** — confirm the recipient has Outlook before sending one.
- For long-term universal storage (e.g. evidence archiving), choose `.html`, or use "Print（打印）" → a virtual printer to output as PDF.

## 5.5 How to Archive Emails?

### 5.5.1 What Is Archiving?

Archiving moves **old emails from the mailbox into a local `.pst` data file**, freeing up server mailbox space. Archived emails can still be viewed and searched in the archive data file on Outlook's left side.

### 5.5.2 Step 1: Create a .pst Data File

1. Click **File（文件）**.

![[ch5-file-tab-ribbon.png]]

2. On the "Info（信息）" page, click **Account Settings（帐户设置）** → **Account Settings（帐户设置(A)...）**.

![[ch5-account-settings-menu.png]]

3. In the window that pops up, switch to the **Data Files（数据文件）** tab and click **Add（添加(A)...）**.

![[ch5-data-files-add.png]]

4. Choose a save location and name it (e.g. "My Outlook Data File.pst（我的 Outlook 数据文件.pst）"), then click OK. The new .pst appears in the data file list.

![[ch5-new-pst-listed.png]]

**Note**: this `.pst` is the "container" for archived emails — save it on a **non-system drive**.

### 5.5.3 Step 2: Run the Archive

1. Click **File（文件）** → **Info（信息）** → **Tools（工具）** → **Clean Up Old Items（清理旧项目(C)...）**.

![[ch5-tools-cleanup-old-items.png|431]]

2. In the "Archive（存档）" dialog:
   - Select **Archive this folder and all subfolders（将该文件夹及其子文件夹存档）** and choose the folder to archive in the list (e.g. "Inbox（收件箱）").
   - Set the date for **Archive items older than（将早于该时间的项目存档）** (only emails older than this date get archived).
   - At "Archive file（存档文件）", click **Browse（浏览(B)...）** and select the .pst file created in the previous step.

![[ch5-archive-dialog.png|355]]

![[ch5-archive-browse-pst.png|581]]

3. Click **OK（确定）** to start archiving. During archiving, the status bar shows progress (e.g. "Archiving Inbox（正在存档收件箱）").

![[ch5-archive-progress.png]]

**Note**: archiving **moves**, not copies — after archiving, the original emails are removed from the mailbox and can only be viewed in the .pst.

### 5.5.4 Step 3: Close and Reopen the Archive File

- **Close**: in the left folder list, right-click the .pst data file → **Close "My Outlook Data File"（关闭"我的 Outlook 数据文件"）**. This only hides it from Outlook; the file stays on your hard drive.

![[ch5-close-pst-context-menu.png]]

- **Reopen**: click **File（文件）** → **Open & Export（打开和导出）** → **Open Outlook Data File（打开 Outlook 数据文件）**, and select the .pst file to view archived emails again.

![[ch5-open-outlook-data-file.png]]

### 5.5.5 Bonus: AutoArchive

Besides manual archiving, you can have Outlook archive automatically on a schedule:

1. Click **File（文件）** → **Options（选项）** → **Advanced（高级）** → **AutoArchive Settings（自动存档设置）**.
2. Check "Run AutoArchive every N days（每隔 N 天运行自动存档）", and set the archive period, the criteria for old emails, and the `.pst` save location.

**Note**: AutoArchive likewise moves emails into a local `.pst`; the backup requirements are the same as manual archiving (see 5.5.6).

### 5.5.6 Notes

- **The new .pst is saved only on your local hard drive**: when you reinstall your computer later, you must copy the .pst file beforehand to a non-system drive / USB drive / cloud drive, or all archived emails will be lost (see [[#10.1 Back Up Email Archives]]).
- Archiving is a move operation — confirm you picked the right target folder before archiving.
- Archiving of corporate Exchange mailboxes may be taken over by administrator policies (e.g. server-side archiving), in which case local archiving may be unavailable.

## 5.6 How to Search for the Emails You Need?

### 5.6.1 Instant Search Box

1. Click the "Search（搜索）" box at the top of the window (or press `Ctrl` + `E`).

![[ch5-instant-search-box.png]]

2. Type keywords; results are filtered and displayed instantly.
3. In the "Scope（范围）" group of the "Search（搜索）" tab, you can switch the search scope: **Current Folder（当前文件夹） / Subfolders（子文件夹） / Current Mailbox（当前邮箱） / All Mailboxes（所有邮箱） / All Outlook Items（所有 Outlook 项目）**.

### 5.6.2 Search Tools Tab

After clicking the search box, a **Search（搜索）** tab appears on the ribbon, where you can combine filters: From（发件人）, Subject（主题）, Has Attachments（有附件）, Categorized（已分类）, To（收件人）, Unread（未读邮件）, Flagged（已标记）, Important（重要事项）, etc. (the "More（其他）" drop-down has more filters).

![[ch5-search-tools-ribbon.png]]

### 5.6.3 Common Search Syntax

Typing syntax directly in the search box is faster than clicking through filters one by one:

| Syntax | What It Does |
|------|------|
| `from:Zhang San` | Find emails whose sender is Zhang San |
| `subject:report` | Find emails whose subject contains "report" |
| `hasattachments:yes` | Find only emails with attachments |
| `received:>=2026/8/1` | Find emails received after August 1 |
| `hasflag:yes` | Find emails with a Follow-up flag |

**Note**: the date format follows the system regional settings (e.g. `2026/8/1` on a Chinese system); combine multiple conditions with spaces, e.g. `from:Zhang San hasattachments:yes`.

# 6 How to Customize the Calendar?

## 6.1 How to Add a Second Time Zone?

### 6.1.1 What Is a Dual Time Zone?

Show **two time zones side by side** in the time bar on the left of the calendar, making it easy to compare times when scheduling meetings with overseas colleagues — no mental time-difference math.

### 6.1.2 How to Set It Up?

1. Click the **Calendar（日历）** icon at the bottom left of Outlook to switch to calendar view.

![[ch6-calendar-navigation-icon.png|244]]

2. Click **File（文件）** → **Options（选项）**.

![[ch6-file-tab-calendar-view.png]]

![[ch6-backstage-options-button.png|155]]

3. In the "Outlook Options（Outlook 选项）" window, choose **Calendar（日历）** on the left and find the **Time zones（时区）** section.

![[ch6-calendar-options-time-zones.png|513]]

4. Enter a label for the main time zone (e.g. `CN`); check **Show a second time zone（显示附加时区(D)）**, select the other party's time zone (e.g. `(UTC-05:00) Eastern Time (US & Canada)（(UTC-05:00) 东部时间(美国和加拿大)）`) and enter a label (e.g. `USA`). Click **Swap Time Zones（交换时区(S)）** to swap the main/secondary zones.

![[ch6-second-time-zone-enabled.png|507]]

5. Click "OK（确定）".

### 6.1.3 Effect and Notes

After setup, the time zone bar on the left of the calendar shows two zones side by side (the secondary zone on the left, the primary on the right), aligned row by row:

![[ch6-calendar-dual-time-zones.png|383]]

**Note**:
- Appointment times are still interpreted in the **primary time zone**; the secondary zone is only a display reference.
- Use short English abbreviations for labels (e.g. `CN`, `USA`) — the time zone bar is narrow and long labels get cut off.

## 6.2 How to Show the Lunar Calendar and Public Holidays?

### 6.2.1 How to Set It Up?

1. Click **File（文件）** → **Options（选项）**.

![[ch6-file-tab-calendar-view.png]]

![[ch6-backstage-options-button.png|127]]

2. In the "Outlook Options（Outlook 选项）" window, choose **Calendar（日历）** on the left, and make the following two settings in the **Calendar options（日历选项）** section.

3. **Show the lunar calendar**: check **Enable an alternate calendar（启用备用日历(E)）**, and set the two drop-downs to **Chinese (Simplified)（中文(简体)）** and **Lunar Calendar（农历）**. The lunar date then appears next to calendar dates.

![[ch6-alternate-calendar-lunar.png]]

4. **Add public holidays**: click **Add Holidays（添加假日(A)...）**.

![[ch6-add-holidays-button.png|485]]

5. In the "Add Holidays to Calendar（将假日添加到日历）" dialog, check **China（中国）** and click "OK（确定）" to import.

![[ch6-add-holidays-china.png]]

### 6.2.2 Notes

- Holidays appear on the calendar as **all-day events**.
- **Don't import repeatedly**: adding the same country's holidays twice causes duplicate display; if duplicated, you can only delete them manually in the calendar.
- The alternate calendar only affects display; it doesn't change the Gregorian dates used by appointments.

## 6.3 How to Change Working Hours?

### 6.3.1 How to Set It Up?

1. Click **File（文件）** → **Options（选项）**.

![[ch6-file-tab-calendar-view.png]]

![[ch6-backstage-options-button.png|109]]

2. In the "Outlook Options（Outlook 选项）" window, choose **Calendar（日历）** on the left and find the **Work time（工作时间）** section.

![[ch6-work-time-settings.png|530]]

3. In the "Work time（工作时间）" section, set:
   - **Start time（开始时间(T)） / End time（结束时间(E)）**: e.g. 8:00–17:00.
   - **Work week（工作周）**: check Monday through Friday.
   - **First day of week（一周的第一天(D)）**: choose per your habit (e.g. Monday).
   - **First week of year（一年的第一周(Y)）**: e.g. "Starts on Jan 1（开始于一月一日）".
4. Click "OK（确定）".

### 6.3.2 Notes

- Working hours affect the **background shading of working hours** in the calendar (non-working hours show as grey).
- When colleagues in your organization check your free/busy times with the **Scheduling Assistant（日程安排助理）**, this is also the reference (see [[#7.1.1 How to View Attendees' Available Times?]]).

## 6.4 How to Show Week Numbers on the Calendar?

### 6.4.1 How to Set It Up?

1. Click **File（文件）** → **Options（选项）**.

![[ch6-file-tab-calendar-view.png]]

![[ch6-backstage-options-button.png|109]]

2. In the "Outlook Options（Outlook 选项）" window, choose **Calendar（日历）** on the left, and in the **Display options（显示选项）** section check **Show week numbers in the month view and in the Date Navigator（在月视图和日期选择区中显示周数(N)）**.

![[ch6-show-week-numbers-option.png]]

3. Click "OK（确定）".

### 6.4.2 Effect and Use

After setup, each row in the month view shows a week number on its left (e.g. "Week 36（36 周）", "Week 37（37 周）"), and the Date Navigator on the left shows them too:

![[ch6-calendar-week-numbers.png]]

**Use**: great for people who schedule work by "week number", such as school teaching weeks or project iteration weeks.

# 7 How to Create and Manage Meeting Invitations?

## 7.1 How to Create a Meeting Invitation?

1. Switch to calendar view, click the **Home（开始）** tab → **New Meeting（新建会议）** (or press `Ctrl` + `Shift` + `Q`).

![[ch7-new-meeting-button.png]]

2. In the meeting window, fill in: **Title（标题(L)）**, **Required（必需(U)）** attendees, **Optional（可选(P)）** attendees, **Start time（开始时间(T)） / End time（结束时间(D)）**, **Location（位置）**, and the body.

![[ch7-new-meeting-window.png]]

3. Click **Send（发送(S)）**, and the attendees receive the meeting invitation email.

**Note**: the difference between "Required（必需）" and "Optional（可选）" is like To vs. CC in emails — Required are the main attendees, Optional can come or not; both receive the invitation.

### 7.1.1 How to View Attendees' Available Times?

1. In the meeting window, click the **Scheduling Assistant（日程安排助理）** tab.

![[ch7-scheduling-assistant-tab.png]]

2. After adding attendees, the grid shows each person's free/busy times (dark blue means **busy**; the legend also includes tentative, out of office, working elsewhere, no information, outside of working hours), grouped on the left by **Required Attendees（必需的与会者） / Optional Attendees（可选的与会者） / Resources (room or equipment)（资源(房间或设备)）**.
3. Drag in the grid to select a time when everyone is free, or click **AutoPick（自动选取）** to let Outlook automatically find the next time everyone is available.

![[ch7-scheduling-assistant-autopick.png|646]]

**Note**: the Scheduling Assistant's free/busy lookup depends on the other party recording their schedule in Outlook Calendar; an empty calendar (no information) doesn't mean they're actually free.

### 7.1.2 How to Book a Meeting Room?

1. In the meeting window, click the **Rooms（位置）** button (or **Add Rooms（添加会议室）** in the "Scheduling Assistant（日程安排助理）" tab).

![[ch7-select-rooms-dialog.png|611]]

2. In the **Select Rooms（选择会议室）** dialog that pops up (in an Exchange environment, choosing "All Rooms" in the address book lists meeting-room resource mailboxes), pick a room with suitable capacity and location, and add it to the **Rooms（会议室(R)）** field.
3. The room is added as a **resource attendee** and automatically accepts or declines the invitation based on conflicts.

**Note**: the meeting-room feature requires the administrator to configure resource mailboxes beforehand; also remember to confirm in the Scheduling Assistant that the room itself isn't occupied.

## 7.2 How to Respond to a Meeting Invitation?

After opening the invitation email, the "Respond（响应）" group has four buttons:

![[ch7-meeting-response-buttons.png]]

| Response | Meaning |
|------|------|
| Accept（接受） | Confirm attendance; the meeting enters your calendar |
| Tentative（暂定） | Might attend; marked as tentative in the calendar |
| Decline（谢绝） | Not attending; the meeting doesn't enter the calendar |
| Propose New Time（建议新时间） | The original time doesn't work; propose another time to the organizer |

Click the drop-down arrow to the right of a button — each response offers three reply methods:

![[ch7-meeting-response-options.png]]

- **Edit the response before sending（发送前编辑答复(E)）**: attach a note before sending.
- **Send the response now（立即发送答复(S)）**: send directly without writing anything.
- **Do not send a response（不发送答复(D)）**: only update your own calendar without notifying the organizer.

**Note**:

- After accepting, the meeting enters your calendar automatically — no need to add it manually.
- When a conflict prevents attendance, it's more polite to click **Propose New Time（建议新时间）** or explain in the response than to decline outright.
- If you choose "Do not send a response（不发送答复）", the organizer can't see your status (see [[#7.3 How to Check Attendees' Responses?]]) — for important meetings, it's still better to send a response.

## 7.3 How to Check Attendees' Responses?

1. The organizer **double-clicks the meeting** in their own calendar.
2. Click **Tracking（跟踪）** (or "Tracking（跟踪）" in the "Meeting（会议）" tab).
3. The list shows each attendee's status: **Accepted（接受） / Tentative（暂定） / Declined（拒绝） / No Response（未响应）**.

**Note**:

- **Only the organizer** can see the Tracking page; regular attendees cannot.
- If an attendee chose "Do not send a response（不发送响应）" when responding, the organizer keeps seeing "No Response（无响应）" — it doesn't mean they haven't seen it.

## 7.4 How to Modify a Meeting Invitation?

1. The organizer double-clicks the meeting in the calendar and modifies the time, location, or content.
2. Click **Send Update（发送更新）** — all attendees receive the update notice and their calendars sync automatically.

**Note**:

- **Only the organizer** can modify the meeting; attendees can only change notes/reminders in their own calendars.
- When an attendee saves after adding personal notes, they can choose **not to send updates** (to avoid disturbing others).
- To cancel a meeting, use the **Cancel Meeting（取消会议）** button and send the cancellation notice; the meeting is removed from everyone's calendar.

# 8 How to Manage Contacts?

## 8.1 Outlook Address Books and Their Differences?

| Type | Storage Location | Characteristics |
|------|---------|------|
| Contacts（联系人） | Local personal address book | Created and maintained by yourself; can add/delete/edit; lost when reinstalling the computer (export a backup) |
| Global Address List (GAL)（全球通讯簿） | Exchange server | The organization's full roster, maintained by the administrator; **read-only** — you can't add to it yourself |
| Auto-Complete List（自动完成列表） | Local cache | The history suggestions that pop up when entering recipients, accumulated automatically with use |

**Note**: external contacts (customers, suppliers, etc.) are not in the GAL — add them manually to "Contacts（联系人）" (see 8.2).

## 8.2 How to Add External Contacts to the Local Address Book?

**Method 1: Create Manually**

1. Switch to the **People（人员）** view (left navigation pane).
2. Click **New Contact（新建联系人）** and fill in name, email, phone, company, etc.
3. Click "Save & Close（保存并关闭）".

**Method 2: Add from a Received Email (Recommended)**

1. Open an email from the person.
2. **Right-click the sender's address** → choose **Add to Outlook Contacts（添加到 Outlook 联系人）**.
3. The email address is filled in automatically; add the other info and save.

**Note**: Method 2 is the fastest and avoids mistyping the address; add the name and company promptly for easier searching later.

## 8.3 How to Create a Local Contact Group?

1. In the **People（人员）** view, click **New Contact Group（新建联系人组）**.
2. Enter a group name (e.g. "Project Team（项目组）").
3. Click **Add Members（添加成员）** — choose from the address book or create new contacts to join.
4. Click "Save & Close（保存并关闭）".

**Use**: when emailing a group of people, just type the group name in the To field; when membership changes, you only update the group, not every email.

**Note**:

- A contact group is **visible only to you** and stored in your local contacts.
- Recipients who expand the group name can see all member addresses in it; if privacy matters, use BCC instead (see [[#3.2 Difference Between To（收件人） / CC（抄送） / BCC（密件抄送）]]).

## 8.4 How to Export and Import the Local Address Book?

**Export:**

1. Click **File（文件）** → **Open & Export（打开和导出）** → **Import/Export（导入/导出）**.
2. Choose **Export to a file（导出到文件）** → **Comma Separated Values（逗号分隔值）(CSV)**.
3. Select the **Contacts（联系人）** folder, specify a save location, and finish the export.

**Import:**

1. In the same wizard, choose **Import from another program or file（从另一程序或文件导入）** → **Comma Separated Values（逗号分隔值）**.
2. Select the CSV file, **map fields** as needed, and finish the import.

**Note**: this backup is a must before reinstalling your computer (see [[#10.2 Exporting and Re-importing Local Contacts When Reinstalling]]); CSV files can be opened and edited in Excel, good for batch cleanup before re-importing.

# 9 Essential Skills for an Assistant

## 9.1 How to Make Emails from Your Boss Display in Green?

1. In the Inbox, click **View（视图）** → **View Settings（视图设置）** → **Conditional Formatting（条件格式）**.
2. Click **Add（添加）** and name the rule (e.g. "Boss（老板）").
3. Click **Font（字体）** and set the color to green.
4. Click **Condition（条件）** and enter the boss's name or email in "From（发件人）".
5. Click "OK（确定）" all the way through — emails from your boss will show in green, instantly recognizable.

**Note**: conditional formatting rules are **saved per view** and affect only the current view; you can set other colors for important clients the same way.

## 9.2 How to Set Up Delegate Access on Your Boss's Outlook?

Perform the following steps on **your boss's own computer**:

1. Click **File（文件）** → **Info（信息）** → **Account Settings（帐户设置）** → **Delegate Access（代理人访问）**.
2. Click **Add（添加）** and select the assistant's name.
3. Set permission levels for Calendar, Tasks, Inbox, etc.:

| Permission Level | What They Can Do |
|---------|---------|
| Reviewer（审阅者） | View only, no changes |
| Author（作者） | View and create items (e.g. create appointments on their behalf) |
| Editor（编辑者） | View, create, modify, and delete |

**Note**: the delegation applies to **the boss's own mailbox**, not the assistant's; this feature is only supported in Exchange environments.

## 9.3 How to View Your Boss's Calendar?

Perform the following steps on **the assistant's computer**:

1. Switch to the **Calendar（日历）** view.
2. Click **Open Calendar（打开日历）** → **Open Shared Calendar（打开共享日历）**.
3. Enter the boss's name or email and click "OK（确定）".

**Note**:

- Prerequisite: the boss has granted access per 9.2 (calendar permission at least "Reviewer（审阅者）").
- Once opened, the boss's calendar appears in the "Shared Calendars（共享日历）" group and can be shown **side by side or overlaid** with yours for easy comparison.

## 9.4 How to Send Email on Behalf of Your Boss?

1. Open a **new email**.
2. Click the **Options（选项）** tab and enable the **From（发件人）** field.
3. Select the boss's mailbox in the From field.
4. Compose and send normally.

**Note**:

- Prerequisite: the boss has granted **Send on Behalf（代表发送）** permission.
- Recipients see the sender as **"Assistant on behalf of Boss（助理 代表 老板）"**.
- To send fully as the boss (without the "on behalf of" label), you need **Send As（发送身份）** permission, configured by the Exchange administrator.

# 10 Things to Watch Out for When Reinstalling Your Computer

## 10.1 Back Up Email Archives

**Method 1: Export to .pst**

1. Click **File（文件）** → **Open & Export（打开和导出）** → **Import/Export（导入/导出）**.
2. Choose **Export to a file（导出到文件）** → **Outlook Data File (.pst)（Outlook 数据文件(.pst)）**.
3. Check the folders to back up (can include subfolders), specify a save location, and finish the export.

**Method 2: Copy the .pst File Directly**

1. Click **File（文件）** → **Info（信息）** → **Account Settings（帐户设置）** → **Data Files（数据文件）** to see the actual path of the .pst file.
2. **Close Outlook**, then copy the .pst file from that path to your backup location.

**Note**: emails in an Exchange mailbox are stored on the server and sync after reconfiguring the account post-reinstall; but **local archive .pst files, rules, and signatures** exist only locally and must be backed up manually.

## 10.2 Exporting and Re-importing Local Contacts When Reinstalling

See [[#8.4 How to Export and Import the Local Address Book?]]: export "Contacts（联系人）" to CSV as a backup before reinstalling, and import with the same wizard after reinstalling.

**Note**: put the exported CSV on a **non-system drive, USB drive, or cloud drive** — reinstalling the system wipes the system drive.

## 10.3 Re-create Email Signatures After Reinstalling

Signatures are stored locally (`%APPDATA%\Microsoft\Signatures`) and are lost after reinstalling; re-create them per [[#2.1 What Is an Email Signature and How to Customize It?]].

**Tip**: before reinstalling, you can **back up the whole Signatures folder**; after reinstalling, copy it back to the original path and your signatures are restored without rebuilding.

[[Microsoft Outlook-中文版|中文版 →]]
