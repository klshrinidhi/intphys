#include "ScreenshotManager.h"



TArray<TSharedPtr<FScreenshot>> UScreenshotManager::Screenshots{};


bool UScreenshotManager::Initialize(
    int Width, int Height, int NumFrames,
    TArray<AActor*>& OriginActors,
    int32 RandomSeed,
    bool Verbose)
{
   FIntVector Size(Width, Height, NumFrames);
   for(auto& OriginActor : OriginActors)
       Screenshots.Emplace(new FScreenshot(Size, OriginActor, RandomSeed, Verbose));
   return true;
}


bool UScreenshotManager::Capture(const TArray<AActor*>& IgnoredActors)
{
    for(auto& Screenshot : Screenshots)
	if(!Screenshot->Capture(IgnoredActors))
	    return false;
    return true;
}

bool UScreenshotManager::Save(const FString& Directory, TArray<FString>& OutActorsMasks)
{
    for(int32 Idx=0; Idx<Screenshots.Num(); ++Idx)
    {
	auto OutDirectory = FPaths::Combine(Directory, FString::Printf(TEXT("%02d"), Idx));
	if(!Screenshots[Idx]->Save(OutDirectory, OutActorsMasks))
	    return false;
    }
    return true;
}


void UScreenshotManager::Reset(bool DeleteActors)
{
    for(auto& Screenshot : Screenshots)
	Screenshot->Reset(DeleteActors);
}


void UScreenshotManager::SetOriginActors(TArray<AActor*>& Actors)
{
    verifyf(Screenshots.Num() == Actors.Num(),
	    TEXT("Number of Actors should equal number of screenshots"));
    for(int32 Idx=0; Idx<Screenshots.Num(); ++Idx)
	Screenshots[Idx]->SetOriginActor(Actors[Idx]);
}


bool UScreenshotManager::IsActorInFrame(AActor* Actor, int FrameIndex)
{
    for(auto& Screenshot : Screenshots)
	if(!Screenshot->IsActorInFrame(Actor, static_cast<uint>(FrameIndex)))
	    return false;
    return true;
}


bool UScreenshotManager::IsActorVisible(AActor* Actor, const TArray<AActor*>& IgnoredActors)
{
    for(auto& Screenshot : Screenshots)
	if(!Screenshot->IsActorVisible(Actor, IgnoredActors))
	    return false;
    return true;
}
