#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monster World IV (메가드라이브) 한글화 패치 적용 도구
사용법: python apply_patch.py <원본_일본어판_ROM_경로> [-o 출력경로] [-f]
"""

import argparse
import hashlib
import os
import struct
import sys

# 필수 원본 및 결과 롬 해시 (GRCh/MD 표준)
EXPECTED_ORIGINAL_SHA256 = "3796F407AE0BF3B74BBE53335ADF57F295F0BF53EF7D82B603AC73350EAC8CAE"
EXPECTED_PATCHED_SHA256 = "7095A4A82AC132DEDE3A42CD6A77D9E568AC1C801F84A8B239AB96093345E398"
EXPECTED_ROM_SIZE = 2097152  # 정확히 2,097,152 바이트 (2MB)

def compute_sha256(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest().upper()

def apply_ips(base_data: bytes, ips_data: bytes) -> bytes:
    """표준 IPS 패치 적용 루틴"""
    if ips_data[:5] != b"PATCH":
        raise ValueError("유효하지 않은 IPS 패치 파일입니다 (헤더 오류).")
    
    patched = bytearray(base_data)
    idx = 5
    ips_len = len(ips_data)
    
    while idx < ips_len:
        if ips_data[idx:idx+3] == b"EOF":
            break
        offset = (ips_data[idx] << 16) | (ips_data[idx+1] << 8) | ips_data[idx+2]
        size = (ips_data[idx+3] << 8) | ips_data[idx+4]
        idx += 5
        
        if size == 0:  # RLE 레코드
            rle_size = (ips_data[idx] << 8) | ips_data[idx+1]
            val = ips_data[idx+2]
            idx += 3
            # 확장 필요 시 확장
            if offset + rle_size > len(patched):
                patched.extend(b"\x00" * (offset + rle_size - len(patched)))
            patched[offset : offset + rle_size] = bytes([val] * rle_size)
        else:  # 일반 레코드
            chunk = ips_data[idx : idx + size]
            idx += size
            if offset + size > len(patched):
                patched.extend(b"\x00" * (offset + size - len(patched)))
            patched[offset : offset + size] = chunk

    return bytes(patched)

def main():
    parser = argparse.ArgumentParser(
        description="Monster World IV (메가드라이브) 한글화 패치 적용 스크립트"
    )
    parser.add_argument("rom", help="일본어 원본 ROM 파일 경로 (.md / .bin)")
    parser.add_argument("-p", "--patch", default=None, help="IPS 패치 파일 경로 (기본값: monster4_ko.ips)")
    parser.add_argument("-o", "--output", default="Monster World IV (Korean).md", help="출력할 한글화 ROM 파일 경로")
    parser.add_argument("-f", "--force", action="store_true", help="출력 파일이 이미 존재하는 경우 덮어쓰기 허용")

    args = parser.parse_args()

    # 1. 입력 롬 파일 확인
    if not os.path.exists(args.rom):
        print(f"[오류] 지정한 원본 ROM 파일을 찾을 수 없습니다: {args.rom}", file=sys.stderr)
        sys.exit(1)

    # 2. 출력 파일 중복 확인
    if os.path.exists(args.output) and not args.force:
        print(f"[오류] 출력 파일이 이미 존재합니다: {args.output}", file=sys.stderr)
        print("덮어쓰려면 -f 또는 --force 옵션을 사용하십시오.", file=sys.stderr)
        sys.exit(1)

    # 3. IPS 패치 파일 경로 결정
    patch_path = args.patch
    if patch_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        patch_path = os.path.join(script_dir, "monster4_ko.ips")

    if not os.path.exists(patch_path):
        print(f"[오류] IPS 패치 파일을 찾을 수 없습니다: {patch_path}", file=sys.stderr)
        sys.exit(1)

    # 4. 원본 롬 무결성 검사 (읽기 전용)
    with open(args.rom, "rb") as f:
        orig_data = f.read()

    orig_sha = compute_sha256(orig_data)
    print(f"[검사] 원본 ROM 파일 크기: {len(orig_data):,} 바이트")
    print(f"[검사] 원본 ROM SHA256: {orig_sha}")

    if orig_sha != EXPECTED_ORIGINAL_SHA256:
        print("[오류] 입력한 ROM이 일치하지 않습니다! 패치 적용이 중단됩니다.", file=sys.stderr)
        print(f"  - 올바른 원본 롬: Monster World IV (Japan) [GM G-5519-01]", file=sys.stderr)
        print(f"  - 필수 SHA256: {EXPECTED_ORIGINAL_SHA256}", file=sys.stderr)
        print(f"  - 입력 파일 SHA256: {orig_sha}", file=sys.stderr)
        print("※ 미국판(VC판), 프로토타입 또는 비공식 덤프는 지원되지 않습니다.", file=sys.stderr)
        sys.exit(1)

    print("[통과] 일본어 원본 정품 카트리지 ROM이 정상 확인되었습니다.")

    # 5. 패치 파일 로드
    with open(patch_path, "rb") as f:
        ips_data = f.read()
    print(f"[로드] 패치 파일: {patch_path} ({len(ips_data):,} 바이트)")

    # 6. 패치 적용
    patched_data = apply_ips(orig_data, ips_data)

    # 7. 패치 결과 검증
    patched_sha = compute_sha256(patched_data)
    if len(patched_data) != EXPECTED_ROM_SIZE:
        print(f"[오류] 패치 결과 롬 크기가 비정상적입니다: {len(patched_data):,} 바이트", file=sys.stderr)
        sys.exit(1)

    if patched_sha != EXPECTED_PATCHED_SHA256:
        print("[오류] 패치 결과 ROM의 해시 검증에 실패했습니다!", file=sys.stderr)
        print(f"  - 기대 SHA256: {EXPECTED_PATCHED_SHA256}", file=sys.stderr)
        print(f"  - 실제 SHA256: {patched_sha}", file=sys.stderr)
        sys.exit(1)

    print(f"[성공] 한글화 ROM 검증 완료: SHA256 {patched_sha}")

    # 8. 출력 파일 저장
    with open(args.output, "wb") as f:
        f.write(patched_data)

    print(f"[완료] 한글화 ROM이 성공적으로 생성되었습니다: {args.output}")

if __name__ == "__main__":
    main()
