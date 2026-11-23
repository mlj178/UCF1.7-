using UnityEngine;
using UnityEngine.UI;

public class HUD_KillMark : Singleton<HUD_KillMark>
{
	public delegate void KillMarkEvent(ref EventData killMarkEvtData);

	public struct EventData
	{
		public Player killer;

		public Player dead;

		public int multiKill;

		public ShowType showType;

		public DamageType dmgType;
	}

	public enum ShowType
	{
		Normal = 0,
		OnlyVoice = 1,
		None = 2
	}

	public KillMarkAsset asset;

	[SerializeField]
	private CommonKillMark commonMark;

	[SerializeField]
	private RectTransform multiKillEffect;

	[SerializeField]
	private RawImage multiKillEffectImage;

	[SerializeField]
	private CommonKillMark specialKill;

	[SerializeField]
	private AudioSource voiceAudioSource;

	public CharacterVoice voiceAsset;

	public static readonly int FirstKill;

	public static readonly int LastKill;

	public static readonly int Revenge;

	public static KillMarkEvent KillMarkEvent_Listener;

	private void Start()
	{
	}

	protected override void OnDestroy()
	{
	}

	public void PlayCommonMark(ShowType showType, int multiKill, HeadShotType headShot, bool wallThrough, DamageType damageType, bool isVVIP)
	{
	}

	public void PlayCommonMark(Texture tex)
	{
	}

	public void PlayMultiKillEffect()
	{
	}

	public void DeathEvent(DeathEventData eventData)
	{
	}
}
