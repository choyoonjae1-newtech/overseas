#!/bin/bash

# AX Oversea 빠른 배포 스크립트

set -e

echo "🚀 AX Oversea 배포 준비 중..."

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Git 상태 확인
if [ ! -d .git ]; then
    echo -e "${YELLOW}⚠️  Git 저장소가 초기화되지 않았습니다.${NC}"
    echo "Git을 초기화하시겠습니까? (y/n)"
    read -r answer
    if [ "$answer" = "y" ]; then
        git init
        echo -e "${GREEN}✅ Git 저장소 초기화 완료${NC}"
    else
        echo -e "${RED}❌ 배포를 위해서는 Git이 필요합니다.${NC}"
        exit 1
    fi
fi

# .env 파일 확인
if [ ! -f backend/.env ]; then
    echo -e "${YELLOW}⚠️  backend/.env 파일이 없습니다.${NC}"
    echo ".env.example을 복사하여 .env를 생성하시겠습니까? (y/n)"
    read -r answer
    if [ "$answer" = "y" ]; then
        cp backend/.env.example backend/.env
        echo -e "${GREEN}✅ .env 파일 생성 완료${NC}"
        echo -e "${YELLOW}📝 backend/.env 파일을 열어 API 키를 설정하세요!${NC}"
        exit 0
    fi
fi

# 변경사항 확인
if [[ `git status --porcelain` ]]; then
    echo -e "${YELLOW}📝 변경된 파일:${NC}"
    git status --short
    
    echo ""
    echo "커밋 메시지를 입력하세요:"
    read -r commit_message
    
    if [ -z "$commit_message" ]; then
        commit_message="Update: $(date '+%Y-%m-%d %H:%M')"
    fi
    
    git add .
    git commit -m "$commit_message"
    echo -e "${GREEN}✅ 커밋 완료${NC}"
else
    echo -e "${GREEN}✅ 변경사항 없음${NC}"
fi

# 원격 저장소 확인
if git remote -v | grep -q 'origin'; then
    echo -e "${GREEN}✅ 원격 저장소 연결됨${NC}"
    
    echo ""
    echo "GitHub에 푸시하시겠습니까? (y/n)"
    read -r answer
    if [ "$answer" = "y" ]; then
        git push origin main
        echo -e "${GREEN}✅ 푸시 완료!${NC}"
        echo ""
        echo -e "${GREEN}🎉 배포 완료!${NC}"
        echo "Railway와 Vercel에서 자동 배포가 시작됩니다."
        echo ""
        echo "배포 상태 확인:"
        echo "  Railway: https://railway.app/dashboard"
        echo "  Vercel:  https://vercel.com/dashboard"
    fi
else
    echo -e "${YELLOW}⚠️  원격 저장소가 설정되지 않았습니다.${NC}"
    echo "GitHub 저장소 URL을 입력하세요 (예: https://github.com/username/ax-oversea.git):"
    read -r repo_url
    
    if [ ! -z "$repo_url" ]; then
        git remote add origin "$repo_url"
        git branch -M main
        git push -u origin main
        echo -e "${GREEN}✅ 원격 저장소 설정 및 푸시 완료!${NC}"
    fi
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}배포 완료!${NC}"
echo -e "${GREEN}========================================${NC}"
