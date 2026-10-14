"""Tests des utilitaires de parsing Wi-Fi."""
import wifi_backend as wb


class TestChannelToBand:
    def test_2_4_ghz(self):
        for ch in [1, 6, 9, 11, 13, 14]:
            assert wb.channel_to_band(ch) == "2.4 GHz"

    def test_5_ghz(self):
        for ch in [36, 44, 100, 149, 165, 177]:
            assert wb.channel_to_band(ch) == "5 GHz"

    def test_6_ghz(self):
        for ch in [181, 200, 233]:
            assert wb.channel_to_band(ch) == "6 GHz"

    def test_invalid(self):
        assert wb.channel_to_band("") == ""
        assert wb.channel_to_band(None) == ""
        assert wb.channel_to_band("abc") == ""
        assert wb.channel_to_band("250") == ""

    def test_string_input(self):
        assert wb.channel_to_band("11") == "2.4 GHz"
        assert wb.channel_to_band(" 36 ") == "5 GHz"


class TestParseProfilesWindows:
    def test_french_format(self):
        raw = (
            "\r\nProfils sur l'interface Wi-Fi\u00a0: \r\n\r\n"
            "Profils utilisateurs\r\n-------------\r\n"
            "    Tous les profils utilisateur    \u00a0: MonSSID\r\n"
            "    Tous les profils utilisateur    \u00a0: AutreWifi\r\n"
        )
        result = wb._parse_profiles_windows(raw)
        assert result == ["MonSSID", "AutreWifi"]

    def test_english_format(self):
        raw = (
            "\r\nProfiles on interface Wi-Fi:\r\n\r\n"
            "User profiles\r\n-------------\r\n"
            "    All User Profile     : MySSID\r\n"
            "    All User Profile     : OtherWifi\r\n"
        )
        result = wb._parse_profiles_windows(raw)
        assert result == ["MySSID", "OtherWifi"]

    def test_empty_section(self):
        raw = (
            "\r\nProfils sur l'interface Wi-Fi\u00a0: \r\n\r\n"
            "Profils de stratégies de groupe (lecture seule)\r\n"
            "-----------------------------------------------\r\n"
            "    <Aucun>\r\n"
        )
        assert wb._parse_profiles_windows(raw) == []

    def test_deduplication(self):
        raw = (
            "    Profil : MonSSID\r\n"
            "    Profil : MonSSID\r\n"
            "    Profil : Autre\r\n"
        )
        assert wb._parse_profiles_windows(raw) == ["MonSSID", "Autre"]

    def test_ssid_with_colon(self):
        raw = "    Profil : Maison:5G\r\n"
        assert wb._parse_profiles_windows(raw) == ["Maison:5G"]

    def test_non_indented_ignored(self):
        raw = (
            "Profils utilisateurs\r\n"      # pas indenté → ignoré
            "    Profil : Valide\r\n"
        )
        assert wb._parse_profiles_windows(raw) == ["Valide"]


class TestCleanNetshLine:
    def test_nbsp_replacement(self):
        assert wb._clean_netsh_line("Nom\u00a0: test") == "Nom : test"

    def test_bom_removal(self):
        assert wb._clean_netsh_line("\ufeffSSID") == "SSID"

    def test_tab_conversion(self):
        assert wb._clean_netsh_line("a\tb") == "a    b"


class TestDecode:
    def test_utf8(self):
        assert wb._decode("héllo".encode("utf-8")) == "héllo"

    def test_cp850(self):
        # Le caractère 'é' en CP850 est 0x82
        assert "é" in wb._decode(b"\x82")

    def test_empty(self):
        assert wb._decode(b"") == ""