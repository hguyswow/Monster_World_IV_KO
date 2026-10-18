# 몬스터 월드 IV (Monster World IV) 메가드라이브 한글화 패치

1994년 세가(SEGA)/웨스톤(Westone)의 메가드라이브 액션 RPG **『몬스터 월드 IV (Monster World IV)』** 일본어판 롬을 한국어로 바꾸는 비공식 IPS 패치입니다. 롬은 포함되어 있지 않습니다.


## 스크린샷 / Screenshots

| | |
|---|---|
| ![title](screenshots/01_title.png) 타이틀 | ![intro](screenshots/02_dialog_intro.png) 도입부 대사 |
| ![yesno](screenshots/03_save_yes_no.png) 저장 / 예·아니오 메뉴 | ![palace](screenshots/04_dialog_palace.png) 궁전 대사 |
| ![menu](screenshots/05_equipment_menu.png) 장비 메뉴 | ![credit](screenshots/06_credit_dialog.png) 제작자 표시 |

*Screenshots are from an emulator (BizHawk). Game graphics (c) SEGA / Westone. This repository contains no ROM.*


## 1. 필요한 원본 롬

- 일본어판 `Monster World IV (Japan)`, 카트리지 번호 **GM G-5519**
- 파일 크기 정확히 `2,097,152` 바이트, 헤더 체크섬 `0x77AE`
- **SHA256**: `3796F407AE0BF3B74BBE53335ADF57F295F0BF53EF7D82B603AC73350EAC8CAE`

미국/유럽 버추얼 콘솔판, 영문 패치본, 크기나 해시가 다른 덤프에는 적용되지 않으며 자동으로 거부됩니다.

## 2. 패키지 구성

- `monster4_ko.ips`: IPS 패치 (69,067 바이트)
- `apply_patch.py`: 원본 롬 검증 + 패치 적용 + 결과 검증 (파이썬 3.8 이상, 표준 라이브러리만 사용)
- `CHECKSUMS.txt`: SHA256 목록
- `FONT_LICENSE_NeoDunggeunmo_OFL.txt`: 한글 글리프 폰트의 라이선스 전문 (SIL OFL 1.1)
- `README_ko.md`: 이 문서

## 3. 적용 방법

```bash
python apply_patch.py "경로/Monster World IV (Japan).md"
python apply_patch.py "경로/Monster World IV (Japan).md" -o "경로/mw4ko.md"   # 출력 경로 지정
python apply_patch.py "경로/Monster World IV (Japan).md" -f                   # 기존 파일 덮어쓰기
```

적용이 끝나면 결과 롬을 자동 검증합니다.
- 크기 `2,097,152` 바이트, 헤더 체크섬 `0x5D76`
- **SHA256**: `7095A4A82AC132DEDE3A42CD6A77D9E568AC1C801F84A8B239AB96093345E398`

온라인 IPS 패처나 Lunar IPS 로 `monster4_ko.ips` 를 직접 적용해도 같은 롬이 만들어집니다.

## 4. 번역 내용

- 제작자: `KOREAN:hguyswow` (타이틀 화면 중앙 하단 저작권 표기 바로 아래 및 도입부 아버지 대사에 표시)
- 대사 268개 한글화 (해요체 중심, 아샤/페페로그 이름 치환 연동) — 269번째(`dialog_268`)는 미번역
- 장비/아이템 130개 이름·설명, 지명 8개, 시스템 메시지 31개, 이름·사운드 테스트 문구 한글화
- 타이틀 메뉴 `NEW GAME` → `새 게임` (`이어하기` 스프라이트도 같은 방식으로 교체)
- 68000 게임 코드는 한 바이트도 바꾸지 않았고, 대사/폰트/문자열 데이터와 포인터, 헤더 체크섬만 변경됩니다.

## 5. 폰트 고지 (Neo둥근모, SIL OFL 1.1)

한글 16x16 글리프는 **Neo둥근모(Neo Dunggeunmo)** 에서 래스터화했습니다.
Based on glyphs by Eunbin Jeong (Dalgona.), SIL Open Font License 1.1.
Copyright (c) 2017-2021, Eunbin Jeong (Dalgona.). 라이선스 전문은 `FONT_LICENSE_NeoDunggeunmo_OFL.txt` 를 보세요.
이 패치에서 폰트 파생 비트맵 부분은 OFL 1.1 조건을 따르며, 이 패치는 폰트 이름을 내세우지 않는 별개의 수정물입니다.

## 6. 알려진 한계

1. `dialog_268` 한 건은 번역되지 않았습니다.
2. 상점/주민의 2회차 이상 분기 대사와 타이틀 `이어하기`(세이브가 있을 때 나타남)는 실엔진에서 확인하지 못했습니다.
3. 그림으로 된 글자(타이틀 로고, 저작권 표기, `PRESS START`, 메뉴의 `Equipment`/`Item`)는 원작 그대로 영문입니다.
4. 예/아니오 선택창의 하이라이트 폭이 글자 폭과 맞지 않을 수 있습니다.
5. 확인한 환경은 에뮬레이터(BizHawk 2.11.1, Genesis Plus GX 코어)뿐이며 실기와 플래시카트는 미검증입니다.

## 7. 플래시카트 사용 팁 (MD v3 Pro 등, 미검증 일반 팁)

- 롬 파일명은 짧고 단순하게(영문/숫자) 바꾸고 확장자는 `.md` 또는 `.bin` 으로 출력하세요 (`-o mw4ko.md`).
- 이 게임은 SRAM 세이브를 씁니다. 카트에서 세이브가 실제로 저장/불러오기 되는지 먼저 확인하세요.

## 8. 저작권 및 면책

- 롬 파일은 포함하지 않습니다. 본인이 합법적으로 가진 카트리지에서 덤프한 롬에만 사용하세요.
- 몬스터 월드 IV의 저작권은 SEGA 및 Westone 에 있습니다.
- 이 패치로 생기는 어떤 손해에도 제작자는 책임지지 않습니다.
