import smtplib
import imaplib
import json
import time
from pathlib import Path
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
CONFIG_PATH = Path(__file__).with_name("config.json")

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
    """Récupère le lien modifiable à la main dans config.json."""
    try:
        payload = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        link = str(payload.get("formation_link") or "").strip()
        if link:
            return link
    except Exception as exc:
        print(f"⚠️ Impossible de lire config.json, fallback utilisé: {exc}")
    return DEFAULT_FORMATION_LINK


def generer_contenu_html(formation_link):
    """Génère le contenu HTML du mail de rappel 5 minutes - Style Sales Hacking responsive"""
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
                content: '⚡';
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
            .urgency-badge {
                display: inline-block;
                background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
                color: #ffffff;
                padding: 8px 20px;
                border-radius: 25px;
                font-size: 14px;
                font-weight: 600;
                margin-bottom: 25px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
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
                font-size: 24px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-align: center;
                margin: 0 0 40px 0;
                font-weight: 700;
                line-height: 1.3;
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
            .countdown-box {
                background: linear-gradient(135deg, rgba(255, 107, 107, 0.1) 0%, rgba(255, 142, 142, 0.1) 100%);
                border: 2px solid #ff6b6b;
                border-radius: 15px;
                padding: 25px;
                margin: 30px 0;
                text-align: center;
            }
            .countdown-text {
                font-size: 20px;
                color: #ff6b6b;
                font-weight: 700;
                margin: 0;
            }
            .cta-container {
                text-align: center;
                margin: 50px 0;
            }
            .cta-button {
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                color: #ffffff !important;
                padding: 22px 50px;
                text-decoration: none;
                font-size: 18px;
                font-weight: 700;
                border-radius: 30px;
                transition: all 0.3s ease;
                letter-spacing: 0.3px;
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
                border: none;
                text-transform: uppercase;
                animation: glow 2s ease-in-out infinite alternate;
            }
            @keyframes glow {
                from { box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4); }
                to { box-shadow: 0 8px 35px rgba(102, 126, 234, 0.6); }
            }
            .cta-button:hover {
                transform: translateY(-3px);
                box-shadow: 0 12px 30px rgba(102, 126, 234, 0.5);
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
                font-weight: 600;
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
                    font-size: 36px;
                }
                .sub-headline {
                    font-size: 22px;
                }
                .body-text {
                    font-size: 16px;
                }
                .cta-button {
                    padding: 20px 45px;
                    font-size: 17px;
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
                    font-size: 20px;
                    margin-bottom: 30px;
                }
                .body-text {
                    font-size: 15px;
                    line-height: 1.6;
                    margin-bottom: 25px;
                    text-align: justify;
                }
                .countdown-box {
                    padding: 20px;
                    margin: 25px 0;
                }
                .countdown-text {
                    font-size: 18px;
                }
                .cta-container {
                    margin: 35px 0;
                }
                .cta-button {
                    padding: 18px 35px;
                    font-size: 16px;
                    display: block;
                    width: calc(100% - 70px);
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
                
                <h1 class="primary-headline">C'est parti !</h1>
                
                
                <p class="body-text">
                    Le cours de formation TP CRCD démarre dans 5 minutes ! 
                    Connectez-vous dès maintenant à la plateforme pour ne rien manquer 
                    de cette session interactive.
                </p>
                
                <div class="cta-container">
                    <a href="__FORMATION_LINK__" 
                       class="cta-button" target="_blank">
                         Se connecter maintenant
                    </a>
                </div>
                
                <p class="body-text">
                    Si vous rencontrez des difficultés techniques, contactez-nous immédiatement !
                </p>
                
                <p class="closing-text">On vous attend ! </p>
                <p class="signature">L'équipe Sales Hacking</p>
            </div>
            
            <div class="footer">
                <p><strong>Sales Hacking</strong> - Formation Interactive</p>
                <p>© 2025 Sales Hacking. Tous droits réservés.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content.replace("__FORMATION_LINK__", formation_link)


def envoyer_rappel_5min():
    """Envoie le rappel 5 minutes avant le début du cours"""
    print(
        f"⚡ Envoi du rappel 5 minutes - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    sender = username
    subject = "Le cours commence dans 5 minutes ! Connectez-vous maintenant"
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

            print(f"✅ Rappel 5min envoyé à {destinataire}")
            envois_reussis += 1

            # Pause entre les envois
            time.sleep(1)

        except Exception as e:
            print(f"❌ Erreur pour {destinataire}: {e}")
            envois_echoues += 1

    print(
        f"📊 Résumé rappel 5min: {envois_reussis} envois réussis, {envois_echoues} échecs"
    )


if __name__ == "__main__":
    envoyer_rappel_5min()
