using UnityEngine;
using UnityEngine.UI;

public class HUD_WeaponSlotIndividual : MonoBehaviour
{
	private RawImage slotImage;

	private RectTransform slotRect;

	[SerializeField]
	private RawImage weaponImage;

	[SerializeField]
	private RawImage extraImage;

	private static readonly Vector2 wpnOriginPos;

	private static readonly Vector2 wpnOffsetPos;

	public Color curColor { get; private set; }

	private void Awake()
	{
	}

	private void Update()
	{
	}

	public void SetSprite(WpnSpriteAsset spriteAsset)
	{
	}

	public void Clean()
	{
	}

	public void ForwardAnim()
	{
	}

	public void BackAnim()
	{
	}
}
