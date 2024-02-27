

def get_event_descriptions(): # Security ID'lerin açıklamaları
    event_descriptions = {
    4624: "Successful user logon",
    4625: "Failed user logon attempt",
    4634: "User logoff",
    4648: "A privileged service was called",
    4672: "Special privileges assigned to new logon",
    4688: "A new process has been created",
    4697: "Changes have been made to an audited system configuration",
    4700: "A user account's password was changed",
    5379: "Initiating a computer account management or service initiation operation",
    6406: "A new process has started or a session has been initiated",
    6407: "A process has ended or a session has been terminated",
    5024: "The Windows Firewall Service has started successfully",
    5033: "The Windows Firewall Service has failed to start",
    4902: "The Per-user audit policy table was created",
    4608: "Windows is starting up",
    4826: "Boot Configuration Data was modified",
    4696: "A primary token was assigned to process",
    1100: "The event logging service has shut down",
    4738: "A user account was changed",
    5059: "A change has been made to Windows Firewall exception list",
    4798: "A user account was created",
    4799: "A user account was deleted",
    5382: "User performed a security ID override",
    4905: "Security event source unregister attempt",
    1101: "An event logged when the audit log is cleared",
    4616: "A system time change event",
    4904: "Windows Firewall Activation process",
    4647: "An account successfully logged on",
    4797: "Network policy change successful",
    5058: "Windows Defender SmartScreen prevented an unrecognized app from starting.",
    5061: "Password change process is being monitored"
    }
    return event_descriptions

# Örnek olarak belirli bir Security ID'ye erişmek için:
# security_id_4624_aciklama = security_ids.get(4624)
# print("4624 Security ID'sinin açıklaması:", security_id_4624_aciklama)

"""
    4624: "Başarılı bir kullanıcı oturum açma işlemi",
    4625: "Başarısız bir kullanıcı oturum açma denemesi",
    4634: "Bir kullanıcı oturumu kapatıldı",
    4648: "Bir hesap üzerinde başka bir kullanıcı tarafından bir yetki ıskartası yapıldı",
    4672: "Bir hesap üzerinde yetki talebi yapıldı",
    4688: "Bir yeni süreç oluşturuldu",
    4697: "Sistemde bir yapılandırma değişikliği yapıldı",
    4700: "Bir hesabın parolası değiştirildi",
    5379: "Girişimci bir bilgisayar hesabı işlemi veya servis başlatma olayı.",
    6406: "İşlem başlatıldı, izlenmeye başladı veya oturum açıldı.",
    6407: "İşlem sonlandırıldı veya oturum kapatıldı.",
    5024: "Bir güvenlik politikası uygulandı veya güncellendi.",
    5033: "Bir hesap başarısız oturum açma denemesi yaptı.",
    4902: "Bir bağlamda bir servis oluşturuldu veya başlatıldı.",
    4608: "Bir kullanıcı oturum açtı veya başka bir kullanıcı oturum açtı.",
    4826: "Bir güvenlik ID'si değiştirildi veya sıfırlandı.",
    4696: "Bir birimde izleme başlatıldı veya durduruldu.",
    1100: "Event Log servisi başladı veya durduruldu.",
    4738: "Bir kullanıcı hesabının bir grup üyeliği değiştirildi.",
    5059: "Bir ağ politikası başarılı bir şekilde güncellendi.",
    4798: "Bir hizmet bir kullanıcı hesabını başarıyla oluşturdu.",
    4799: "Bir hizmet bir kullanıcı hesabını başarıyla sildi.",
    5382: "Bir kullanıcı veya bilgisayar hesabı bir güvenlik kimliği sildi."
    1101: "Denetim günlüğü temizlendiğinde kaydedilen bir olay",
    4616: "Sistem zamanının değiştirilmesi olayı",
    4904: "Windows Firewall Etkinleştirme İşlemi",
    4647: "Hesap başarıyla oturum açtı",
    4797: "Ağ ilkesi değişikliği başarılı"
    5058: "Windows Defender SmartScreen, tanınmayan bir uygulamanın başlamasını engelledi"
    5061: "Şifre Değiştirme İşlemi İzleniyor"
"""
