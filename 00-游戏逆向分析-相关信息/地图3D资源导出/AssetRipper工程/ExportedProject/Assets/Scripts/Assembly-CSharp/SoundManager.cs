using System.Collections.Generic;
using UnityEngine;

public class SoundManager : Singleton<SoundManager>
{
	public GameObject soundObj;

	private SimpleObjectPool soundPool;

	[SerializeField]
	private GameObject channelSoundPrefab;

	private Dictionary<string, ChannelSound> channels;

	private Dictionary<AudioClip, float> _2dSndTempDic;

	private static Dictionary<string, SO_2dSound> _2dSnd;

	private static Dictionary<string, SO_3dSound> _3dSnd;

	public static readonly Vector2 CommonSndDistance;

	protected override void Awake()
	{
	}

	public static void Play2DSound(string name, int index = -1, bool temp = false)
	{
	}

	public static RecyclableSound Play2DSound(AudioClip audioClip, int priority = 75)
	{
		return null;
	}

	public static void PlayNotifySound()
	{
	}

	public static void PlayMarkSound()
	{
	}

	public static bool TryCreateChannel(string channelName, out ChannelSound sound)
	{
		sound = null;
		return false;
	}

	public static void Play3DSound(string name, Vector3 worldPos, int index = -1)
	{
	}

	public static RecyclableSound Play3DSound(string name, Transform parent, int index = -1, int priorityOffset = 0)
	{
		return null;
	}

	public static void Play3DSound(AudioClip clip, Vector2 distance, Transform parent, int priority = 128)
	{
	}

	public static void Play3DSound(AudioClip clip, Vector3 worldPos, int priority = 128)
	{
	}

	public static RecyclableSound GetSound()
	{
		return null;
	}

	private static bool TrySet2dData(RecyclableSound sound, string name, int index = -1)
	{
		return false;
	}

	private static bool TrySet3dData(RecyclableSound sound, string name, int index = -1)
	{
		return false;
	}
}
