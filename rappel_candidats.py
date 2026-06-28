import smtplib
import imaplib
import json
import os
import sys
import time
import urllib.request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import make_msgid
from datetime import datetime

# Configuration email
smtp_server = "mail.infomaniak.com"
smtp_port = 465
imap_server = "mail.infomaniak.com"
imap_port = 993
username = "secretariat@saleshacking.fr"
password = "Secretariat75@"
DEFAULT_FORMATION_LINK = "https://socrate-backend-v-hgeeg0anbtddb9cy.francecentral-01.azurewebsites.net/"
FORMATION_PLATFORM_ID = os.environ.get("FORMATION_PLATFORM_ID") or (sys.argv[1] if len(sys.argv) > 1 else "1")
FORMATION_LINK_API_URL = os.environ.get(
    "FORMATION_LINK_API_URL",
    f"{DEFAULT_FORMATION_LINK.rstrip('/')}/api/public/email-formation-link?platform_id={FORMATION_PLATFORM_ID}",
)

# Liste des destinataires (ajoutez/supprimez selon vos besoins)
DESTINATAIRES = [
    "guentas.n@auditsenergies.com",
    "boungo.m@auditsenergies.com",
    "hamzarhaimi5@gmail.com",
    "ben_khalifa423@hotmail.fr",
    "wided@nova-sas.fr",
    "zaki@nova-sas.fr",
]


def get_formation_link():
    """Récupère le lien configuré depuis la plateforme, avec fallback local."""
    try:
        with urllib.request.urlopen(FORMATION_LINK_API_URL, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8"))
            link = str(payload.get("url") or "").strip()
            if payload.get("success") and link:
                return link
    except Exception as exc:
        print(f"⚠️ Impossible de récupérer le lien plateforme, fallback utilisé: {exc}")
    return DEFAULT_FORMATION_LINK


def generer_contenu_html(formation_link):
    """Génère le contenu HTML du mail de rappel - Style Sales Hacking responsive"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                color: #333333;
                min-height: 100vh;
                padding: 20px 0;
            }
            
            /* DESKTOP - Styles par défaut */
            .email-container {
                max-width: 750px;
                margin: 0 auto;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                padding: 50px 40px;
                text-align: center;
                position: relative;
                overflow: hidden;
                border-radius: 20px 20px 0 0;
                margin: 0 40px;
            }
            .header::before {
                content: '🚀';
                position: absolute;
                font-size: 80px;
                top: 15px;
                right: 40px;
                opacity: 0.3;
                transform: rotate(15deg);
            }
            .header::after {
                content: '';
                position: absolute;
                top: -50px;
                left: -50px;
                width: 120px;
                height: 120px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 50%;
            }
            .logo {
                color: #ffffff;
                font-size: 32px;
                font-weight: 700;
                margin: 0;
                letter-spacing: 0.5px;
                position: relative;
                z-index: 1;
            }
            .logo-icon {
                display: inline-block;
                margin-right: 15px;
                font-size: 28px;
            }
            .content-card {
                background-color: #ffffff;
                margin: 0 40px;
                padding: 60px 50px;
                border-radius: 0 0 20px 20px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
                position: relative;
                overflow: hidden;
            }
            .content-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
            }
            .primary-headline {
                font-size: 42px;
                font-weight: 700;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-align: center;
                margin: 0 0 30px 0;
                line-height: 1.2;
            }
            .sub-headline {
                font-size: 20px;
                color: #666666;
                text-align: center;
                margin: 0 0 50px 0;
                font-weight: 500;
                line-height: 1.4;
            }
            .body-text {
                font-size: 17px;
                color: #000000;
                line-height: 1.7;
                margin: 0 0 35px 0;
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
                text-align: justify;
                font-weight: 700;
            }
            .bullet-list {
                margin: 40px 0;
                padding: 0;
                list-style: none;
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
            }
            .bullet-item {
                display: flex;
                align-items: flex-start;
                margin: 18px 0;
                font-size: 17px;
                color: #000000;
                line-height: 1.6;
                padding: 15px 25px;
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(240, 147, 251, 0.1) 100%);
                border-radius: 12px;
                border-left: 4px solid #f093fb;
            }
            .bullet-point {
                width: 10px;
                height: 10px;
                background: linear-gradient(135deg, #667eea, #f093fb);
                border-radius: 50%;
                margin-right: 18px;
                margin-top: 8px;
                flex-shrink: 0;
            }
            .cta-container {
                text-align: center;
                margin: 50px 0;
            }
            .cta-button {
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                color: #ffffff !important;
                padding: 20px 45px;
                text-decoration: none;
                font-size: 17px;
                font-weight: 600;
                border-radius: 25px;
                transition: all 0.3s ease;
                letter-spacing: 0.3px;
                box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
                border: none;
            }
            .cta-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
                text-decoration: none;
                color: #ffffff !important;
            }
            .cta-button:visited, .cta-button:link {
                color: #ffffff !important;
            }
            .closing-text {
                font-size: 17px;
                color: #000000;
                line-height: 1.6;
                margin: 40px 0 20px 0;
                text-align: center;
            }
            .signature {
                font-size: 17px;
                background: linear-gradient(135deg, #667eea, #f093fb);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-weight: 600;
                margin: 20px 0 0 0;
                text-align: center;
            }
            .footer {
                background-color: #ffffff;
                margin: 20px 40px 0 40px;
                padding: 30px 20px;
                text-align: center;
                color: #666666;
                font-size: 14px;
                line-height: 1.5;
                border-radius: 15px;
                box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
                border-top: 3px solid #f093fb;
            }
            .footer strong {
                color: #333333;
            }
            
            /* TABLETTE - Écrans moyens (768px à 1024px) */
            @media only screen and (max-width: 1024px) and (min-width: 768px) {
                .email-container {
                    max-width: 650px;
                }
                .header {
                    padding: 40px 30px;
                    margin: 0 30px;
                }
                .logo {
                    font-size: 30px;
                }
                .content-card {
                    margin: 0 30px;
                    padding: 50px 40px;
                }
                .footer {
                    margin: 20px 30px 0 30px;
                }
                .primary-headline {
                    font-size: 38px;
                }
                .sub-headline {
                    font-size: 19px;
                }
                .body-text {
                    font-size: 16px;
                }
                .bullet-item {
                    font-size: 16px;
                    padding: 14px 22px;
                }
                .cta-button {
                    padding: 18px 40px;
                    font-size: 16px;
                }
            }
            
            /* MOBILE - Petits écrans (jusqu'à 767px) */
            @media only screen and (max-width: 767px) {
                body {
                    padding: 10px 0;
                }
                .email-container {
                    margin: 0;
                    max-width: 100%;
                }
                .header {
                    padding: 30px 20px;
                    margin: 0 15px;
                }
                .header::before {
                    font-size: 50px;
                    top: 15px;
                    right: 20px;
                }
                .header::after {
                    width: 80px;
                    height: 80px;
                    top: -40px;
                    left: -40px;
                }
                .logo {
                    font-size: 24px;
                }
                .logo-icon {
                    font-size: 22px;
                    margin-right: 10px;
                }
                .content-card {
                    margin: 0 15px;
                    padding: 35px 25px;
                    border-radius: 0 0 15px 15px;
                }
                .footer {
                    margin: 15px 15px 0 15px;
                    padding: 25px 15px;
                    font-size: 12px;
                }
                .primary-headline {
                    font-size: 28px;
                    margin-bottom: 20px;
                }
                .sub-headline {
                    font-size: 16px;
                    margin-bottom: 35px;
                }
                .body-text {
                    font-size: 15px;
                    line-height: 1.6;
                    margin-bottom: 25px;
                    text-align: justify;
                }
                .bullet-list {
                    margin: 30px 0;
                }
                .bullet-item {
                    font-size: 15px;
                    padding: 12px 18px;
                    margin: 12px 0;
                }
                .bullet-point {
                    width: 8px;
                    height: 8px;
                    margin-right: 15px;
                }
                .cta-container {
                    margin: 35px 0;
                }
                .cta-button {
                    padding: 16px 30px;
                    font-size: 15px;
                    display: block;
                    width: calc(100% - 60px);
                    text-align: center;
                }
                .closing-text {
                    font-size: 15px;
                    margin: 30px 0 15px 0;
                }
                .signature {
                    font-size: 15px;
                }
            }
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <h1 class="logo">
                    <span class="logo-icon"></span>TP CRCD
                </h1>
            </div>
            
            <div class="content-card">
                <p class="body-text">
                    Bonjour ! J'espère que vous allez bien. Comme convenu, votre formation Sales Hacking 
                    aura lieu demain matin à 9h00. Préparez-vous à participer à une session immersive 
                    pour apprendre efficacement !
                </p>
                
                <ul class="bullet-list">
                    <li class="bullet-item">
                        <div class="bullet-point"></div>
                        <span>Connectez-vous 5 minutes avant le début (8h55)</span>
                    </li>
                    <li class="bullet-item">
                        <div class="bullet-point"></div>
                        <span>Préparez votre casque/écouteurs</span>
                    </li>
                    <li class="bullet-item">
                        <div class="bullet-point"></div>
                        <span>Ayez de quoi prendre des notes</span>
                    </li>
                </ul>
                
                <div class="cta-container">
                    <a href="__FORMATION_LINK__" 
                       class="cta-button" target="_blank">
                         Accéder à la plateforme de formation
                    </a>
                </div>
                
                <p class="body-text">
                    Si vous avez des questions ou des difficultés techniques, n'hésitez pas à nous contacter.
                </p>
                
                <p class="closing-text">À demain et bonne soirée !</p>
                <p class="signature">L'équipe Sales Hacking</p>
            </div>
            
            <div class="footer">
                <p><strong>Sales Hacking</strong> - Formations Interactives</p>
                <p>© 2025 Sales Hacking. Tous droits réservés.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content.replace("__FORMATION_LINK__", formation_link)


def envoyer_rappel():
    """Envoie le mail de rappel à tous les destinataires"""
    print(
        f"🚀 Début de l'envoi des rappels - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    sender = username
    subject = "Lien de la session demain matin - Formation TP CRCD"
    formation_link = get_formation_link()
    html_content = generer_contenu_html(formation_link)
    print(f"🔗 Lien formation utilisé: {formation_link}")

    envois_reussis = 0
    envois_echoues = 0

    for destinataire in DESTINATAIRES:
        try:
            # Construction du message
            msg = MIMEMultipart("alternative")
            msg["Message-ID"] = make_msgid()
            msg["Subject"] = subject
            msg["From"] = sender
            msg["To"] = destinataire
            msg.attach(MIMEText(html_content, "html"))
            raw_message = msg.as_string()

            # Envoi SMTP
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
                smtp.login(username, password)
                smtp.sendmail(sender, destinataire, raw_message)

            # Copie dans les messages envoyés
            with imaplib.IMAP4_SSL(imap_server, imap_port) as imap:
                imap.login(username, password)
                imap.append(
                    '"Sent"',
                    "",
                    imaplib.Time2Internaldate(time.time()),
                    raw_message.encode("utf8"),
                )

            print(f"✅ Mail envoyé à {destinataire}")
            envois_reussis += 1

            # Pause entre les envois
            time.sleep(2)

        except Exception as e:
            print(f"❌ Erreur pour {destinataire}: {e}")
            envois_echoues += 1

    print(f"📊 Résumé: {envois_reussis} envois réussis, {envois_echoues} échecs")


if __name__ == "__main__":
    envoyer_rappel()
