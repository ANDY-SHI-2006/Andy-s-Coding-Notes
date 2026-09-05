[Next: Mini Program Configuration →](02-miniprogram-configuration.md)

# 1 Introducing WeChat Mini Programs

This chapter introduces the basic concepts of WeChat Mini Programs, their history, how they differ from traditional apps, and the preparation work before development: registering a Mini Program account, installing WeChat DevTools, and creating your first project.

## 1.1 Mini Program Basics

### 1.1.1 What Is a Mini Program

WeChat Mini Program, or simply "Mini Program" (English name: Mini Program), has a relatively low barrier to entry for developers — it is less difficult than building an app, can satisfy simple basic applications, and is well suited for offline lifestyle-service shops and for converting non-essential, low-frequency use cases.

![[ch01-01.png]]

Software apps installed on phones fall roughly into four categories:

- **Native App**: built for a specific operating system, e.g. iOS (Objective-C), Android (Java, Kotlin), Windows Phone (C#).
- **Web App**: built with H5 + CSS + JavaScript and then packaged into an app, such as an Android `xxx.apk`.
- **Hybrid App**: a mix of native and web.
- **Light App**: a lightweight app hosted inside a super app — a WeChat Mini Program is a light app based on the WeChat app.

### 1.1.2 History of Mini Programs

Timeline of Mini Program development (2016–2024):

| Period | Stage | Description |
| ------ | ----- | ----------- |
| 2016 | Inception | The project was launched and renamed from "App Account" to "Mini Program"; only a small number of developers were invited to the beta — a technology-polishing phase |
| 2017 | Birth | Officially launched on January 9, with basic access, sharing, and QR-scanning features; gradually opened development access to individuals and enterprises |
| 2018 | Feature completion | Added live streaming, message push, and a complete e-commerce chain; shifted from utility apps to commercial-service apps |
| 2019 | Commercialization | Opened ad monetization and search traffic; template-based development became widespread; Mini Programs formally moved toward commercial profitability |
| 2020 | Mass adoption | Driven by the pandemic, lifestyle-service and online-service Mini Programs grew explosively and user numbers peaked |
| 2021–2022 | Ecosystem deepening | Connected traffic across the entire WeChat ecosystem, focused on local brick-and-mortar businesses, and became a core online-operation tool for physical stores |
| 2023–present | Intelligent evolution | Integrated AI technology; lightweight, high-efficiency, and installation-free became the core advantages of Mini Programs |

### 1.1.3 Differences Between Mini Programs and Traditional Apps

| Dimension | Mini Program | Traditional App |
| --------- | ------------ | --------------- |
| Installation | No installation needed; use and go | Must be downloaded and installed from an app store |
| Independence | Depends on a super app (e.g. WeChat) | Standalone app, independent of any platform |
| Development cost | Low (one codebase, runs on multiple platforms) | High (separate iOS and Android versions required) |
| Capability | Limited; depends on the platform's open APIs | Powerful; can call all system capabilities |
| Performance | Close to native, but slightly behind | Best; highly smooth |
| Promotion | Social sharing, QR codes, search | App stores, paid advertising |
| Best for | Lightweight, tool-type, low-frequency businesses that need fast distribution | High-frequency, interaction-heavy, feature-complex businesses pursuing the ultimate experience |

A **Mini Program** is an application that can be used without downloading or installing, hosted by a super app (such as WeChat or Alipay).

- Advantages:
  - **Use and go, no installation**: users don't need to download from an app store — scan a QR code or search to open it; the barrier to use is extremely low.
  - **Low development cost, short cycle**: uses a unified web technology stack (e.g. JS, CSS); one codebase runs cross-platform, greatly reducing development and maintenance costs.
  - **Platform-backed, easy to promote**: backed by high-traffic platforms like WeChat, it can spread virally through sharing, social graphs, and official accounts.
  - **No device adaptation worries**: the runtime environment is provided by the host app (e.g. WeChat), so developers don't need to worry much about compatibility across different phone operating systems.
- Limitations:
  - **Limited features, platform-dependent**: it must rely on the host app (e.g. WeChat) and cannot run independently. Its capabilities are limited to the APIs provided by the platform and cannot achieve every native feature.
  - **Relatively weaker experience**: performance, animation smoothness, and interaction experience are usually not as good as native apps.
  - **Platform rule constraints**: it must comply with the platform's review process, operating rules, and policies, so autonomy is low.

A **traditional app** is a native application that must be downloaded from an app store (such as the App Store or an Android market) and installed onto the phone's operating system.

- Advantages:
  - **Powerful and complete**: can call all of the phone's hardware and system APIs (GPS, Bluetooth, camera, etc.), enabling the most complex and refined features.
  - **Excellent performance, smooth experience**: runs directly on top of the operating system, offering the best response speed, animation, and interaction experience.
  - **Strong independence**: does not depend on any third-party platform; can be operated and branded independently.
  - **Works offline**: core features and content can be packaged inside the app for a better offline experience.
- Limitations:
  - **High development cost, long cycle**: separate iOS and Android development requires significant manpower, time, and funding.
  - **High barrier to promotion and installation**: users must actively search, download, and install from an app store, leading to high acquisition costs and user churn.
  - **Maintenance and updates required**: publishing requires platform review, and version updates must be downloaded manually by users, making maintenance complex.

### 1.1.4 How to Understand Mini Programs

A Mini Program is essentially a lightweight application "embedded" inside a super app (such as WeChat or Alipay). It fulfills the dream of apps being "within reach" — no download or installation needed, just scan or search to open — and it embodies the "use and go" philosophy.

1. **It is not HTML5**: although it uses similar technologies, the experience is much better. It cannot simply be regarded as a mobile web page — it has its own independent runtime environment, feels closer to a native app, and is smoother and more stable than a web page.
2. **Use and go, always at hand**: this is the core characteristic. No download or installation — scan a code or search and use it immediately, close it when done, taking up no phone memory, as convenient as using a tool.
3. **Based on the WeChat client — develop once, run on multiple platforms**: it depends on WeChat as its "host" and cannot exist independently. The benefit is that you develop once and it runs properly on almost every phone with WeChat installed, automatically compatible with different operating systems (iOS/Android), greatly saving development costs.
4. **Elegant user experience**: the Mini Program's design guidelines and runtime mechanism ensure that its smoothness, animations, and overall user experience far exceed ordinary web pages and feel very close to a native app.

### 1.1.5 Who Can Register to Develop Mini Programs

Official documentation: <https://mp.weixin.qq.com/cgi-bin/wx?token=&lang=zh_CN>

Registration is open to: **individuals, enterprises, government bodies, media, and other organizations**.

![[ch01-03.png]]

### 1.1.6 Required Technical Background

Developing Mini Programs requires three basic technologies:

1. **WXSS — responsible for "looking good"**: essentially CSS; controls page styles (colors, layout, fonts, etc.).
2. **WXML — responsible for the "skeleton"**: a markup language similar to HTML; builds page structure and content.
3. **JavaScript — responsible for "making it move"**: handles all business logic, such as click events, data fetching, and page interaction.

### 1.1.7 Mini Program Framework Structure

The Mini Program runtime framework can be divided into three layers:

- **View layer**: composed of WXML, WXSS, JS, and JSON; responsible for rendering page structure and styles.
- **Logic/control layer**: composed of control code and API interfaces; communicates with the view layer in both directions through "reactive data binding" and "events".
- **Operating system layer**: provides low-level capabilities such as network communication, audio recording, data caching, and system information.

![[ch01-04.png]]

From an overall architecture perspective, the client side includes the Mini Program frontend and the WeChat client. The Mini Program frontend architecture consists of WXML, WXSS, JavaScript, and custom components, and connects through WeChat capabilities (WeChat APIs, open capabilities, native components) to backend services (business servers, databases, caching, file storage) and third-party services (cloud development: content security, real-time audio/video, map services), supported by CI/CD, monitoring and alerting, log analysis, and performance optimization for operations and deployment.

![[ch01-34.png]]

### 1.1.8 Official Mini Program Developer Documentation

<https://developers.weixin.qq.com/miniprogram/dev/framework/>

## 1.2 Account and Settings

A Mini Program is a service provided by WeChat, and the official documentation clearly defines the access flow for using Mini Programs:

1. **Register**: register a Mini Program on the WeChat Official Accounts Platform; after registration you can complete your information and develop at the same time.
2. **Complete Mini Program info**: fill in basic information including name, avatar, introduction, and service scope.
3. **Develop the Mini Program**: after binding developers and configuring development information, developers can download DevTools and develop and debug the Mini Program with the development documentation.
4. **Submit for review and publish**: after development is complete, submit the code to the WeChat team for review; once approved it can be published (publishing is not allowed during the public-beta period).

![[ch01-05.png]]

### 1.2.1 Registration

**Go to the registration page**: official documentation <https://mp.weixin.qq.com/cgi-bin/wx?token=&lang=zh_CN>, click "Go to register".

**Fill in the registration information**. Notes:

1. One email address can only register one Mini Program account.
2. An email already registered for an Official Account cannot be used to register a Mini Program.
3. After entering your email, click "Activate email", then log in to your mailbox on the redirected page.
4. Your mailbox will receive a verification code; enter it and then set a password (letters, digits, or English symbols, at least 8 characters, case-sensitive).
5. After setting the password, tick the ☐ in front of the agreement, then click Register.

**Information registration**: select "Individual" as the entity type (individual accounts currently do not support WeChat verification, WeChat Pay, or advanced API capabilities), then fill in the entity information:

- ID card name: cannot be changed once the information is approved.
- ID card number: one ID number can register at most 5 Mini Programs.
- Administrator phone number: use the same phone number bound to your WeChat account; one phone number can register at most 5 Mini Programs.
- SMS verification code: enter the 6-digit code received via SMS.
- Administrator identity verification: scan the QR code with WeChat to verify your identity; that WeChat account will become the Mini Program's administrator.

After confirming the submitted entity information (entity name, entity type), click "Confirm". Once "Information submitted successfully" appears, click "Go to Mini Program" to enter the WeChat Official Accounts Platform and use its features.

### 1.2.2 Login

**Go to the official login page**: <https://mp.weixin.qq.com> — you can log in by scanning the QR code or with your account and password.

After logging in, you may be asked for a second QR-code verification; simply scan it with your bound WeChat account. After successful verification, you enter the Mini Program admin console.

**Complete your personal information first**, working through the "Mini Program release flow":

- **Mini Program info**: complete the basic information such as name, icon, and description. The account name must be 4–30 characters (one Chinese character counts as 2 characters); the avatar image must be png, bmp, jpeg, jpg, or gif, no larger than 2 MB — png is recommended, with a suggested size of 144px × 144px; the introduction must not contain content prohibited by national laws and regulations.
- **Mini Program category**: add the Mini Program's service categories and set the primary category.
- **Mini Program filing (ICP)**: complete the filing information (Mini Program info and categories must be filled in first).
- **WeChat verification**: after verification, the account gains "searchable" and "sharable" capabilities; not completing verification does not affect subsequent version releases.

### 1.2.3 Getting the AppID

Mini Program development depends on the Mini Program's AppID. In the admin console, go to **Development & Services → Development Management → Development Settings**, and under "Developer ID" you can view the current Mini Program's **AppID (Mini Program ID)**, which is needed for development; the same page also lets you generate the **AppSecret (Mini Program secret)**.

### 1.2.4 Version Management

Under **Management → Version Management** you can see three kinds of versions:

- **Online version**: the released version available to all users.
- **Review version**: a version submitted to the WeChat team and pending review before release.
- **Development version**: a version uploaded from DevTools, still in development and debugging.

### 1.2.5 Member Management

Mini Program member management covers project members and trial members.

- **Project members**: members who participate in developing and operating the Mini Program and can log in to the admin console, including operators, developers, and data analysts. The administrator can add and remove project members and set their roles under "Member Management".
- **Trial members**: members who participate in beta testing and can use the trial version of the Mini Program, but are not project members. Both the administrator and project members can add and remove trial members.

## 1.3 DevTools and the Simulator

To help developers build and debug WeChat Mini Programs easily and efficiently, Tencent launched the all-new WeChat DevTools on top of the original Official Account web debugging tool, integrating two development modes: Official Account web debugging and Mini Program debugging.

### 1.3.1 Download and Install the Official DevTools (Required)

Download page: <https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html>

The download page offers three builds:

- **Stable Build**: a beta build whose defects have been fixed and which has been promoted to stable — recommended for daily use.
- **RC Build (pre-release)**: contains major features, has passed internal testing, and is reasonably stable.
- **Nightly Build**: a daily build used to fix defects quickly and ship small features agilely; developer self-tested, with subpar stability.

Download the version matching your operating system (Windows 64, Windows 32, macOS x64, macOS ARM64), then double-click to run the installer and keep clicking Next.

Installation notes:

- Do not install DevTools on the C: drive — WeChat DevTools is demanding on computer performance. It's fine while learning, but the impact becomes noticeable with larger projects later on.
- Make sure to download the correct build for your system; before installing, quit any "PC manager" type utilities, as they can interfere with the installation.
- If your account lacks permissions, remember to run the installer as administrator.

### 1.3.2 Entering the Tool

After opening WeChat DevTools, scan the QR code with your previously bound WeChat account to log in. Once logged in, you officially enter the development management panel. On the left side of the panel you can switch between project types: **Mini Program, Mini Game, Multi-platform App, Code Snippet, Official Account Web, Others**; click "+" to create a new project.

## 1.4 Creating a Project

In the development management panel, select "Mini Program" and click "+" to open the "Create Mini Program" screen. After scanning the QR code with your previously bound WeChat account, fill in the project information:

- **Project name**: can be in Chinese, e.g. `demo`.
- **Directory**: where the project is stored, e.g. `D:\wechatProject`.
- **AppID**: the Mini Program ID obtained in section 1.2.3; if you don't have one, you can register or use a test account instead.
- **Backend service**: choose "WeChat Cloud Development" or "Do not use cloud services" (the default template does not apply to cloud development).
- **Development mode**: select "Mini Program".
- **Template / Language**: choose the development language and template for interaction, e.g. the official "JS Base Template" (language: JavaScript).

Click "Create" to generate your first Mini Program project and preview it in the simulator.

![[ch01-38.png]]

[Next: Mini Program Configuration →](02-miniprogram-configuration.md)
