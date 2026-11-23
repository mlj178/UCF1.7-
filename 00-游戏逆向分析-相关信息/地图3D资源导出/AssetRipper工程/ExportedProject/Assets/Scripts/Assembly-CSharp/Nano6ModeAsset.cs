using System;
using UnityEngine;

[CreateAssetMenu]
public class Nano6ModeAsset : NanoModeAsset
{
	[Serializable]
	public struct UpgradeAsset
	{
		[Serializable]
		public enum TargetPos
		{
			Ammo = 0,
			Character = 1,
			Radar = 2,
			HPRegen = 3,
			ThermalVision = 4
		}

		public Sprite[] textSprite;

		public Sprite[] iconSprite;

		public TargetPos[] iconAnimTarget;
	}

	public AudioClip[] soldierRadio;

	public AudioClip[] nanoGhostRadio;

	public float[] soldierExpPerInfect;

	public UpgradeAsset up_Soldier_1;

	public UpgradeAsset up_Soldier_2;

	public UpgradeAsset up_Nano_1;

	public UpgradeAsset up_Nano_2;

	public Texture skillTip_GhostBlade;

	public Texture skillTip_ArmoredTerminator;

	public Sprite[] nanoClothCount;

	public AudioClip pickUpSupplyBox;
}
