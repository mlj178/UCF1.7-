using UnityEngine;
using UnityEngine.UI;

public class HUD_SpectateMsg : MonoBehaviour
{
	[SerializeField]
	private RawImage levelIcon;

	[SerializeField]
	private RectTransform rect;

	[SerializeField]
	private Text nameText;

	[SerializeField]
	private Image killTypeImage;

	[SerializeField]
	private Text damageText;

	private static readonly Color deadColor;

	private static readonly Color aliveColor;

	public int damage
	{
		set
		{
		}
	}

	public bool infect
	{
		set
		{
		}
	}

	public void Init(string nickName, int level)
	{
	}

	public void Kill(Sprite killTypeSprite)
	{
	}

	public void SetPos(int index)
	{
	}
}
